from flask_restx import fields
from src.extensions import api

routine_forexercise_model = api.model("RoutineForExercise", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "estimatedTime": fields.Integer,
    "user_id": fields.Integer,
    "patient_id": fields.Integer
})

exercise_forroutine_model = api.model("ExerciseForRoutine", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "routine_ids": fields.List(fields.Integer)
})


exercise_model = api.model("Exercise", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "routine_ids": fields.List(fields.Integer),
    "routine": fields.List(fields.Nested(routine_forexercise_model))
})


routine_model = api.model("Routine", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "estimatedTime": fields.Integer,
    "user_id": fields.Integer,
    "patient_id": fields.Integer,
    "exercises": fields.List(fields.Nested(exercise_forroutine_model))
})

patient_model = api.model("Patient", {
    "id": fields.Integer,
    "name": fields.String,
    "surname": fields.String,
    "age": fields.Integer,
    "gender": fields.String,
    "routine_id": fields.Integer
})

user_model = api.model("User", {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "password_token": fields.String
})

user_register_model = api.model("UserRegister", {
    "name": fields.String,
    "email": fields.String,
    "password_token": fields.String
})

login_model = api.model("LoginModel", {
    "email": fields.String,
    "password": fields.String
})

logged_model = api.model("LoggedModel", {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "access_token": fields.String
})

success_model = api.model("ChangePasswordModel", {
    "success": fields.Boolean,
})

changePassword_input_model = api.model("ChangePasswordModel", {
    "email": fields.String,
    "newPassword": fields.String
})

patient_input_model = api.model("PatientInputModel", {
    "name": fields.String,
    "surname": fields.String,
    "age": fields.Integer,
    "gender": fields.String,
    "routine_id": fields.Integer
})

addRoutine_input_model = api.model("AddRoutineInputModel", {
    "name": fields.String,
    "description": fields.String,
    "estimatedTime": fields.Integer,
    "user_id": fields.Integer,
    "patient_id": fields.Integer
})

addExerciseToRoutine_input_model = api.model(
    "AddExerciseToRoutineInputModel", {
        "name": fields.String,
        "description": fields.String,
        "routine_name": fields.String
    }
)

exercises_from_routine_model = api.model("ExercisesFromRoutineModel", {
    "name": fields.String,
    "description": fields.String
})
