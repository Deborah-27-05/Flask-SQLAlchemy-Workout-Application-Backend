from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema, exercises_schema,
    workout_schema, workouts_schema,
    workout_exercise_schema, workout_exercise_create_schema
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


# ---------- Exercises ----------

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({'error': 'Exercise not found'}, 404)

    data = exercise_schema.dump(exercise)
    data['workouts'] = workouts_schema.dump(exercise.workouts)
    return make_response(data, 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    json_data = request.get_json()
    try:
        validated = exercise_schema.load(json_data)
    except ValidationError as err:
        return make_response({'errors': err.messages}, 400)

    try:
        exercise = Exercise(**validated)
        db.session.add(exercise)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return make_response({'error': str(e)}, 400)

    return make_response(exercise_schema.dump(exercise), 201)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({'error': 'Exercise not found'}, 404)

    db.session.delete(exercise)
    db.session.commit()
    return make_response({}, 204)


# ---------- Workouts ----------

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({'error': 'Workout not found'}, 404)
    return make_response(workout_schema.dump(workout), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    json_data = request.get_json()
    try:
        validated = workout_schema.load(json_data)
    except ValidationError as err:
        return make_response({'errors': err.messages}, 400)

    try:
        workout = Workout(**validated)
        db.session.add(workout)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return make_response({'error': str(e)}, 400)

    return make_response(workout_schema.dump(workout), 201)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({'error': 'Workout not found'}, 404)

    db.session.delete(workout)
    db.session.commit()
    return make_response({}, 204)


# ---------- Workout <-> Exercise join ----------

@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['POST']
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)

    if not workout:
        return make_response({'error': 'Workout not found'}, 404)
    if not exercise:
        return make_response({'error': 'Exercise not found'}, 404)

    json_data = request.get_json() or {}
    try:
        validated = workout_exercise_create_schema.load(json_data)
    except ValidationError as err:
        return make_response({'errors': err.messages}, 400)

    try:
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            **validated
        )
        db.session.add(workout_exercise)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return make_response({'error': str(e)}, 400)

    return make_response(workout_exercise_schema.dump(workout_exercise), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)