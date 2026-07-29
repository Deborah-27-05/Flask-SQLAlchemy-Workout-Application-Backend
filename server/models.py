from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    # An Exercise has many WorkoutExercises
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan'
    )

    # An Exercise has many Workouts through WorkoutExercises
    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        back_populates='exercises',
        viewonly=True
    )

    VALID_CATEGORIES = ('cardio', 'strength', 'flexibility', 'balance')

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError('Exercise name cannot be empty.')
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        if category not in self.VALID_CATEGORIES:
            raise ValueError(
                f"Category must be one of {self.VALID_CATEGORIES}."
            )
        return category

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )

    # A Workout has many WorkoutExercises
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan'
    )

    # A Workout has many Exercises through WorkoutExercises
    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        back_populates='workouts',
        viewonly=True
    )

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError('duration_minutes must be a positive integer.')
        return value

    def __repr__(self):
        return f'<Workout {self.id}: {self.date}>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    __table_args__ = (
        CheckConstraint(
            'reps IS NULL OR reps > 0', name='check_reps_positive'
        ),
        CheckConstraint(
            'sets IS NULL OR sets > 0', name='check_sets_positive'
        ),
        CheckConstraint(
            'duration_seconds IS NULL OR duration_seconds > 0',
            name='check_duration_seconds_positive'
        ),
        UniqueConstraint(
            'workout_id', 'exercise_id', name='unique_workout_exercise'
        ),
    )

    # A WorkoutExercise belongs to a Workout
    workout = db.relationship('Workout', back_populates='workout_exercises')

    # A WorkoutExercise belongs to an Exercise
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps', 'sets', 'duration_seconds')
    def validate_positive(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f'{key} must be a positive number.')
        return value

    def __repr__(self):
        return (
            f'<WorkoutExercise workout={self.workout_id} '
            f'exercise={self.exercise_id}>'
        )