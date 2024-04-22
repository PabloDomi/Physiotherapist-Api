from flask_restx import fields
from src.extensions import api


exercise_model = api.model("Exercise", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String
})


routine_model = api.model("Routine", {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "estimatedTime": fields.Integer,
    "user_id": fields.Integer,
    "patient_id": fields.Integer,
    "exercises": fields.List(fields.Nested(exercise_model))
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
    "surname": fields.String,
    "username": fields.String,
    "email": fields.String,
    "password_token": fields.String
})
