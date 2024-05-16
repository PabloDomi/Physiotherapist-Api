from src.models.api_models import (
    patient_input_model, success_model
)
from src.models.models import Patient
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

patient_management_ns = Namespace(
    'api/patient_management', authorizations=authorizations
)


@patient_management_ns.route('/registerPatient')
class RegisterPatient(Resource):

    method_decorators = [jwt_required()]

    @patient_management_ns.doc(security='jsonWebToken')
    @patient_management_ns.expect(patient_input_model)
    @patient_management_ns.marshal_list_with(success_model)
    def post(self):

        patient = Patient(
            name=patient_management_ns.payload["name"],
            surname=patient_management_ns.payload["surname"],
            age=patient_management_ns.payload["age"],
            gender=patient_management_ns.payload["gender"]
        )

        db.session.add(patient)
        db.session.commit()
        return {'success': True}, 201


@patient_management_ns.route('/patientDelete/<int:id>')
class PatientDelete(Resource):

    method_decorators = [jwt_required()]

    @patient_management_ns.doc(security='jsonWebToken')
    @patient_management_ns.marshal_list_with(success_model)
    def delete(self, id):
        patient = Patient.query.get(id)
        db.session.delete(patient)
        db.session.commit()
        return {'success': True}, 200
