from src.models.api_models import (
    patient_input_model, success_model, landmarks_model, health_info_model,
    tablet_check_model, tablet_routine_model, tablet_model, tablet_input_model
)
from flask import send_from_directory
from src.models.models import (
    Patient, Routines, updateOnDeleteRoutinePatientId, TabletPatient
)
from src.extensions import db
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required
from pandas import DataFrame
import os

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
        # Iniciar una transacción manualmente
        patient = Patient.query.get(id)
        if not patient:
            return {'message': 'Patient not found'}, 404

        # Obtener y eliminar las rutinas del paciente
        routine = Routines.query.filter_by(patient_id=id).first()

        updateOnDeleteRoutinePatientId(routine)

        db.session.delete(patient)

        # Confirmar la transacción si todo va bien
        db.session.commit()
        return {'success': True}, 200


@patient_management_ns.route('/patientLandmarks')
class patientLandmarks(Resource):

    # method_decorators = [jwt_required()]

    # @patient_management_ns.doc(security='jsonWebToken')

    # Eventualmente se usará la lógica de jwtoken para seguridad

    @patient_management_ns.expect(landmarks_model)
    @patient_management_ns.marshal_list_with(success_model)
    def post(self):
        print(patient_management_ns.payload)
        df = DataFrame(patient_management_ns.payload['landmarks'])
        # Directorio de salida en el contenedor temporal
        output_dir = '/tmp'
        output_file = 'landmarks.csv'

        # Guardar el DataFrame en un archivo CSV en el directorio especificado
        output_path = os.path.join(output_dir, output_file)
        df.to_csv(output_path, index=False)

        print(f'Archivo guardado en {output_path}')

        print('Archivo CSV generado...')
        return 200


@patient_management_ns.route('/download')
class Download(Resource):
    def get(self):
        output_dir = '/tmp'
        output_file = 'landmarks.csv'

        return send_from_directory(output_dir, output_file, as_attachment=True)


@patient_management_ns.route('/patientHealthInfo')
class patientHealthInfo(Resource):

    # method_decorators = [jwt_required()]

    # @patient_management_ns.doc(security='jsonWebToken')

    # Eventualmente se usará la lógica de jwtoken para seguridad

    @patient_management_ns.expect(health_info_model)
    @patient_management_ns.marshal_list_with(success_model)
    def post(self):
        print(patient_management_ns.payload)
        return 200


@patient_management_ns.route('/checkTabletLogin/<int:tablet_id>')
class checkTabletLogin(Resource):

    # method_decorators = [jwt_required()]

    # @patient_management_ns.doc(security='jsonWebToken')

    # Eventualmente se usará la lógica de jwtoken para seguridad

    @patient_management_ns.marshal_list_with(tablet_check_model)
    def get(self, tablet_id):
        tablet = TabletPatient.query.filter_by(id=tablet_id).first()
        if not tablet:
            return {'message': 'Tablet not found'}, 404
        routine = Routines.query.filter_by(
            patient_id=tablet.patient_id
        ).first()
        return {
            'patient_id': tablet.patient_id,
            'treatment_time': tablet.treatment_time,
            'routine_id': routine.id,
            'treatment_cadence': tablet.treatment_cadence
            }, 200


@patient_management_ns.route('/getRoutineById/<string:routine_id>')
class getRoutineById(Resource):

    # method_decorators = [jwt_required()]

    # @patient_management_ns.doc(security='jsonWebToken')
    @patient_management_ns.marshal_with(tablet_routine_model)
    def get(self, routine_id):
        routine = Routines.query.filter_by(id=routine_id).first()
        if routine:
            return routine, 200
        return {'Success': False}, 404


@patient_management_ns.route('/getTablets')
class getTablets(Resource):

    method_decorators = [jwt_required()]

    @patient_management_ns.doc(security='jsonWebToken')
    @patient_management_ns.marshal_list_with(tablet_model)
    def get(self):
        return TabletPatient.query.all()


@patient_management_ns.route('/createTablet')
class createTablet(Resource):

    method_decorators = [jwt_required()]

    @patient_management_ns.doc(security='jsonWebToken')
    @patient_management_ns.expect(tablet_input_model)
    @patient_management_ns.marshal_list_with(success_model)
    def post(self):
        tablet = TabletPatient(
            patient_id=patient_management_ns.payload["patient_id"],
            treatment_time=patient_management_ns.payload["treatment_time"],
            treatment_cadence=patient_management_ns.payload[
                "treatment_cadence"
                ]
        )
        db.session.add(tablet)
        db.session.commit()
        return {'success': True}, 201


@patient_management_ns.route('/deleteTablet/<int:id>')
class deleteTablet(Resource):

    method_decorators = [jwt_required()]

    @patient_management_ns.doc(security='jsonWebToken')
    @patient_management_ns.marshal_list_with(success_model)
    def delete(self, id):
        tablet = TabletPatient.query.get(id)
        if not tablet:
            return {'message': 'Tablet not found'}, 404
        db.session.delete(tablet)
        db.session.commit()
        return {'success': True}, 200


@patient_management_ns.route('/updateTablet')
class updateTablet(Resource):

    method_decorators = [jwt_required()]

    @patient_management_ns.doc(security='jsonWebToken')
    @patient_management_ns.expect(tablet_model)
    @patient_management_ns.marshal_list_with(success_model)
    def put(self):
        tablet = TabletPatient.query.get(
            patient_management_ns.payload["id"]
        )
        if not tablet:
            return {'message': 'Tablet not found'}, 404
        tablet.patient_id = patient_management_ns.payload["patient_id"]
        tablet.treatment_time = patient_management_ns.payload["treatment_time"]
        tablet.treatment_cadence = patient_management_ns.payload[
            "treatment_cadence"
        ]
        db.session.commit()
        return {'success': True}, 200
