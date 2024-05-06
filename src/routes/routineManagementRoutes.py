from src.models.api_models import (
    success_model, addRoutine_input_model
)
from src.models.models import Routines
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
        print(routine_management_ns.payload)

        routine = Routines(
            name=routine_management_ns.payload['name'],
            description=routine_management_ns.payload['description'],
            estimatedTime=routine_management_ns.payload['estimatedTime'],
            user_id=routine_management_ns.payload['user_id'],
            patient_id=routine_management_ns.payload['patient_id']
        )

        db.session.add(routine)
        db.session.commit()
        return {'success': True}, 201
