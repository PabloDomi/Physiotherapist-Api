from src.models.api_models import (
    exercise_model, routine_model, patient_model, user_model
)
from src.models.models import Exercises, Routines, Patient, User
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

ns = Namespace('api', authorizations=authorizations)


@ns.route('/routines')
class RoutineList(Resource):

    method_decorators = [jwt_required()]

    @ns.doc(security='jsonWebToken')
    @ns.marshal_list_with(routine_model)
    def get(self):
        return Routines.query.all()


@ns.route('/exercises')
class ExerciseList(Resource):

    method_decorators = [jwt_required()]

    @ns.doc(security='jsonWebToken')
    @ns.marshal_list_with(exercise_model)
    def get(self):
        return Exercises.query.all()


@ns.route('/patients')
class PatientList(Resource):

    method_decorators = [jwt_required()]

    @ns.doc(security='jsonWebToken')
    @ns.marshal_list_with(patient_model)
    def get(self):
        return Patient.query.all()


@ns.route('/users')
class UserList(Resource):

    method_decorators = [jwt_required()]

    @ns.doc(security='jsonWebToken')
    @ns.marshal_list_with(user_model)
    def get(self):
        return User.query.all()
