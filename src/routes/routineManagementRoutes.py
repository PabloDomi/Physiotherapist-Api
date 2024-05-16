from src.models.api_models import (
    success_model, addRoutine_input_model, addExerciseToRoutine_input_model,
    exercises_from_routine_model, hasRoutine_model, updateRoutine_input_model,
    updateRoutine_model, routine_forexercise_model, exercise_model,
    updateExercise_input_model, updateExercise_model
)
from src.models.models import Routines, Exercises, Patient
from src.extensions import db
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

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

    method_decorators = [jwt_required()]

    @routine_management_ns.doc(security='jsonWebToken')
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

        patient = Patient.query.filter_by(
            id=routine_management_ns.payload['patient_id']
        ).first()

        routineCreated = Routines.query.filter_by(
            name=routine_management_ns.payload['name']
        ).first()

        if patient:
            patient.routine_id = routineCreated.id

        db.session.commit()

        if routine and patient:
            return {'success': True}, 201
        return {'success': False}, 404


@routine_management_ns.route('/addExerciseToRoutine')
class addExerciseToRoutine(Resource):

    method_decorators = [jwt_required()]

    @routine_management_ns.doc(security='jsonWebToken')
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

    method_decorators = [jwt_required()]

    @routine_management_ns.doc(security='jsonWebToken')
    @routine_management_ns.marshal_list_with(exercises_from_routine_model)
    def get(self, routine_name):
        routine = Routines.query.filter_by(name=routine_name).first()
        if routine:
            return routine.exercises, 200
        return {'success': False}, 404


@routine_management_ns.route('/deleteRoutine/<string:routine_id>')
class deleteRoutine(Resource):

    method_decorators = [jwt_required()]

    @routine_management_ns.doc(security='jsonWebToken')
    @routine_management_ns.marshal_with(success_model)
    def delete(self, routine_id):
        routine = Routines.query.filter_by(id=routine_id).first()
        if routine:
            db.session.delete(routine)
            db.session.commit()
            return {'success': True}, 200
        return {'success': False}, 404


@routine_management_ns.route('/checkHasRoutine/<int:patient_id>')
class checkHasRoutine(Resource):

    method_decorators = [jwt_required()]

    @routine_management_ns.doc(security='jsonWebToken')
    @routine_management_ns.marshal_with(hasRoutine_model)
    def get(self, patient_id):
        routine = Routines.query.filter_by(patient_id=patient_id).first()
        if routine:
            return {'hasRoutine': True}, 200
        elif not routine:
            return {'hasRoutine': False}, 200


@routine_management_ns.route('/updateRoutine')
class updateRoutine(Resource):

    method_decorators = [jwt_required()]

    @routine_management_ns.doc(security='jsonWebToken')
    @routine_management_ns.expect(updateRoutine_input_model)
    @routine_management_ns.marshal_with(updateRoutine_model)
    def put(self):

        patient = Patient.query.filter_by(id=routine_management_ns.payload[
            'patient_id'
        ]).first()

        routine = Routines.query.filter_by(id=routine_management_ns.payload[
            'routine_id'
        ]).first()

        initialPatient = Patient.query.filter_by(id=routine.patient_id).first()

        if routine:
            if (routine.name != routine_management_ns.payload['name']):
                routine.name = routine_management_ns.payload['name']

            if (routine.description != routine_management_ns.payload[
                'description'
            ]):
                routine.description = routine_management_ns.payload[
                    'description'
                ]

            if (routine.estimatedTime != routine_management_ns.payload[
                'estimatedTime'
            ]):
                routine.estimatedTime = routine_management_ns.payload[
                    'estimatedTime'
                ]

            if (routine.patient_id != routine_management_ns.payload[
                'patient_id'
            ]):
                initialPatient.routine_id = None

                routine.patient_id = routine_management_ns.payload[
                    'patient_id'
                ]

                if patient:
                    patient.routine_id = routine_management_ns.payload[
                        'routine_id'
                    ]
                else:
                    return {'Success': False}, 404

            db.session.commit()
            return {'Success': True, 'data': routine}, 200

        return {'Success': False}, 404


@routine_management_ns.route('/getRoutineById/<string:routine_id>')
class getRoutineById(Resource):

    method_decorators = [jwt_required()]

    @routine_management_ns.doc(security='jsonWebToken')
    @routine_management_ns.marshal_with(routine_forexercise_model)
    def get(self, routine_id):
        routine = Routines.query.filter_by(id=routine_id).first()
        if routine:
            return routine, 200
        return {'Success': False}, 404


@routine_management_ns.route('/getExerciseById/<string:exercise_id>')
class getExerciseById(Resource):

    method_decorators = [jwt_required()]

    @routine_management_ns.doc(security='jsonWebToken')
    @routine_management_ns.marshal_with(exercise_model)
    def get(self, exercise_id):
        exercise = Exercises.query.filter_by(id=exercise_id).first()
        if exercise:
            return exercise, 200
        return {'Success': False}, 404


@routine_management_ns.route('/deleteExercise/<string:exercise_id>')
class deleteExercise(Resource):

    method_decorators = [jwt_required()]

    @routine_management_ns.doc(security='jsonWebToken')
    @routine_management_ns.marshal_with(success_model)
    def delete(self, exercise_id):
        exercise = Exercises.query.filter_by(id=exercise_id).first()
        if exercise:
            db.session.delete(exercise)
            db.session.commit()
            return {'success': True}, 200
        return {'success': False}, 404


@routine_management_ns.route('/updateExercise')
class updateExercise(Resource):

    method_decorators = [jwt_required()]

    @routine_management_ns.doc(security='jsonWebToken')
    @routine_management_ns.expect(updateExercise_input_model)
    @routine_management_ns.marshal_with(updateExercise_model)
    def put(self):
        exercise = Exercises.query.filter_by(id=routine_management_ns.payload[
            'id'
        ]).first()
        if exercise:
            if (exercise.name != routine_management_ns.payload['name']):
                exercise.name = routine_management_ns.payload['name']

            if (exercise.description != routine_management_ns.payload[
                'description'
            ]):
                exercise.description = routine_management_ns.payload[
                    'description'
                ]

            if (exercise.routine_ids != routine_management_ns.payload[
                'routine_ids'
            ]):
                exercise.routine_ids = routine_management_ns.payload[
                    'routine_ids'
                ]

            db.session.commit()
            return {'Success': True, 'data': exercise}, 200

        return {'Success': False}, 404
