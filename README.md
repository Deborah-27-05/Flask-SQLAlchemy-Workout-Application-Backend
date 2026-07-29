# Workout Tracker API

A Flask + SQLAlchemy + Marshmallow backend for a workout tracking application
used by personal trainers. Tracks workouts, reusable exercises, and the
sets/reps/duration performed for each exercise within a workout.

## Description

- **Exercise**: a reusable exercise definition (name, category, whether
  equipment is needed).
- **Workout**: a single training session (date, duration, notes).
- **WorkoutExercise**: the join between a workout and an exercise, storing
  the reps, sets, and/or duration performed.

A workout has many exercises through workout_exercises, and an exercise can
belong to many workouts through the same join table.

## Installation

```bash
pipenv install
pipenv shell
cd server
flask db init
flask db migrate -m "initial migration"
flask db upgrade head
python seed.py
```

## Running the App

```bash
cd server
flask run -p 5555
```

## Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show a workout, including its workout_exercises (reps/sets/duration + nested exercise) |
| POST | `/workouts` | Create a workout. Body: `{"date": "2026-07-29", "duration_minutes": 45, "notes": "optional"}` |
| DELETE | `/workouts/<id>` | Delete a workout (cascades to its workout_exercises) |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show an exercise and the workouts it belongs to |
| POST | `/exercises` | Create an exercise. Body: `{"name": "Squat", "category": "strength", "equipment_needed": false}` |
| DELETE | `/exercises/<id>` | Delete an exercise (cascades to its workout_exercises) |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout. Body: `{"reps": 12, "sets": 3}` or `{"duration_seconds": 300}` |

Valid `category` values: `cardio`, `strength`, `flexibility`, `balance`.

## Validations

**Table constraints**
- `workouts.duration_minutes` must be greater than 0 (`CheckConstraint`)
- `workout_exercises.reps` / `sets` / `duration_seconds` must be greater than 0 when present
- `workout_exercises` has a unique constraint on `(workout_id, exercise_id)` so the same exercise can't be added to the same workout twice

**Model validations**
- `Exercise.name` cannot be blank
- `Exercise.category` must be one of the valid categories
- `Workout.duration_minutes` must be a positive integer
- `WorkoutExercise.reps` / `sets` / `duration_seconds` must be positive when provided

**Schema validations**
- `Workout.duration_minutes` must be between 1 and 600
- `Exercise.category` must be one of the valid categories (`OneOf`)
- A `WorkoutExercise` must include at least one of reps, sets, or duration_seconds