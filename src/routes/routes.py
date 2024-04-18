from src.models.api_models import exercise_model, routine_model
from src.models.models import Exercises, Routines
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
