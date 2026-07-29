#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print('Clearing existing data...')
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print('Seeding exercises...')
    push_up = Exercise(name='Push-Up', category='strength', equipment_needed=False)
    squat = Exercise(name='Squat', category='strength', equipment_needed=False)
    running = Exercise(name='Running', category='cardio', equipment_needed=False)
    bench_press = Exercise(name='Bench Press', category='strength', equipment_needed=True)
    hamstring_stretch = Exercise(
        name='Hamstring Stretch', category='flexibility', equipment_needed=False
    )

    db.session.add_all([push_up, squat, running, bench_press, hamstring_stretch])
    db.session.commit()

    print('Seeding workouts...')
    workout_1 = Workout(
        date=date(2026, 7, 20),
        duration_minutes=45,
        notes='Upper/lower body strength day'
    )
    workout_2 = Workout(
        date=date(2026, 7, 22),
        duration_minutes=30,
        notes='Cardio and mobility'
    )

    db.session.add_all([workout_1, workout_2])
    db.session.commit()

    print('Seeding workout_exercises...')
    workout_exercises = [
        WorkoutExercise(workout_id=workout_1.id, exercise_id=push_up.id, reps=15, sets=3),
        WorkoutExercise(workout_id=workout_1.id, exercise_id=squat.id, reps=12, sets=4),
        WorkoutExercise(workout_id=workout_1.id, exercise_id=bench_press.id, reps=10, sets=3),
        WorkoutExercise(workout_id=workout_2.id, exercise_id=running.id, duration_seconds=1200),
        WorkoutExercise(
            workout_id=workout_2.id, exercise_id=hamstring_stretch.id, duration_seconds=180
        ),
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()

    print('Done seeding!')