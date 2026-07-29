from marshmallow import Schema, fields, validate, validates_schema, ValidationError

from models import Exercise, Workout, WorkoutExercise


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    category = fields.String(
        required=True,
        validate=validate.OneOf(Exercise.VALID_CATEGORIES)
    )
    equipment_needed = fields.Boolean(required=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(dump_only=True)
    reps = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Integer(allow_none=True, validate=validate.Range(min=1))

    # nested exercise info for display purposes
    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def validate_has_a_metric(self, data, **kwargs):
        if not data.get('reps') and not data.get('sets') and not data.get('duration_seconds'):
            raise ValidationError(
                'At least one of reps, sets, or duration_seconds is required.'
            )


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(
        required=True, validate=validate.Range(min=1, max=600)
    )
    notes = fields.String(allow_none=True, validate=validate.Length(max=1000))

    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema), dump_only=True
    )


class WorkoutExerciseCreateSchema(Schema):
    """Used for the POST body when adding an exercise to a workout."""
    reps = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Integer(allow_none=True, validate=validate.Range(min=1))

    @validates_schema
    def validate_has_a_metric(self, data, **kwargs):
        if not data.get('reps') and not data.get('sets') and not data.get('duration_seconds'):
            raise ValidationError(
                'At least one of reps, sets, or duration_seconds is required.'
            )


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercise_create_schema = WorkoutExerciseCreateSchema()