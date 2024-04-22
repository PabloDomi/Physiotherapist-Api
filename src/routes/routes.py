from src.models.api_models import (
    exercise_model, routine_model, patient_model, user_model
)
from src.models.models import Exercises, Routines, Patient, User
from flask_restx import Resource, Namespace


ns = Namespace('api')


@ns.route('/routines')
class RoutineList(Resource):
    @ns.marshal_list_with(routine_model)
    def get(self):
        return Routines.query.all()


@ns.route('/exercises')
class ExerciseList(Resource):
    @ns.marshal_list_with(exercise_model)
    def get(self):
        return Exercises.query.all()


@ns.route('/patients')
class PatientList(Resource):
    @ns.marshal_list_with(patient_model)
    def get(self):
        return Patient.query.all()


@ns.route('/users')
class UserList(Resource):
    @ns.marshal_list_with(user_model)
    def get(self):
        return User.query.all()
