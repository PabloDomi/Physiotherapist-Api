from src.models.api_models import (
    success_model, addRoutine_input_model, addExerciseToRoutine_input_model,
    exercises_from_routine_model
)
from src.models.models import Routines, Exercises
from src.extensions import db
from flask_restx import Resource, Namespace

authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

routine_management_ns = Namespace(
    'api/routine_management', authorizations=authorizations
)


@routine_management_ns.route('/addRoutine')
class AddRoutine(Resource):
    @routine_management_ns.expect(addRoutine_input_model)
    @routine_management_ns.marshal_with(success_model)
    def post(self):

        routine = Routines(
            name=routine_management_ns.payload['name'],
            description=routine_management_ns.payload['description'],
            estimatedTime=routine_management_ns.payload['estimatedTime'],
            user_id=routine_management_ns.payload['user_id'],
            patient_id=routine_management_ns.payload['patient_id']
        )

        db.session.add(routine)
        db.session.commit()

        if routine:
            return {'success': True}, 201
        return {'success': False}, 404


@routine_management_ns.route('/addExerciseToRoutine')
class addExerciseToRoutine(Resource):
    @routine_management_ns.expect(addExerciseToRoutine_input_model)
    @routine_management_ns.marshal_with(success_model)
    def post(self):

        print(routine_management_ns.payload['routine_name'])

        routine = Routines.query.filter_by(
            name=routine_management_ns.payload['routine_name']
        ).first()

        exercise = Exercises(
            name=routine_management_ns.payload['name'],
            description=routine_management_ns.payload['description'],
            routine_ids=[]
        )

        exercise.routine_ids.append(routine.id)

        db.session.add(exercise)
        db.session.commit()
        if routine and exercise:
            return {'success': True}, 201
        return {'success': False}, 404


@routine_management_ns.route('/getExercisesFromRoutine/<string:routine_name>')
class getExercisesFromRoutine(Resource):
    @routine_management_ns.marshal_list_with(exercises_from_routine_model)
    def get(self, routine_name):
        routine = Routines.query.filter_by(name=routine_name).first()
        if routine:
            return routine.exercises, 200
        return {'success': False}, 404
