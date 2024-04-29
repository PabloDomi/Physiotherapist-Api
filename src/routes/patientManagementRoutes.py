from src.models.api_models import (
    patient_input_model, success_model
)
from src.models.models import Patient
from src.extensions import db
from flask_restx import Resource, Namespace

authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

patient_management_ns = Namespace(
    'api/patient_management', authorizations=authorizations
)


@patient_management_ns.route('/registerPatient')
class RegisterPatient(Resource):
    @patient_management_ns.expect(patient_input_model)
    @patient_management_ns.marshal_list_with(success_model)
    def post(self):
        patient = Patient(
            name=patient_management_ns.payload["name"],
            surname=patient_management_ns.payload["surname"],
            age=patient_management_ns.payload["age"],
            gender=patient_management_ns.payload["gender"],
            routine_id=patient_management_ns.payload["routine_id"]
        )

        db.session.add(patient)
        db.session.commit()
        return {'success': True}, 201
