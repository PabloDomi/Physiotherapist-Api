from src.models.api_models import (
    success_model, changePassword_input_model, error_with_name_model
)
from src.models.models import User, PatientStats, Exercises, Patient
from src.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required


authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

user_management_ns = Namespace(
    'api/user_management', authorizations=authorizations
)


@user_management_ns.route('/changePassword')
class ChangePassword(Resource):

    method_decorators = [jwt_required()]

    @user_management_ns.doc(security='jsonWebToken')
    @user_management_ns.expect(changePassword_input_model)
    @user_management_ns.marshal_list_with(success_model)
    def put(self):
        user = User.query.filter_by(
            email=user_management_ns.payload["email"]
        ).one_or_none()

        if user:
            user.password_token = generate_password_hash(
                user_management_ns.payload["newPassword"]
            )
            db.session.commit()
            return {'success': True}, 201


@user_management_ns.route('/checkEmail/<string:email>')
class CheckEmail(Resource):

    method_decorators = [jwt_required()]

    @user_management_ns.doc(security='jsonWebToken')
    @user_management_ns.marshal_list_with(success_model)
    def get(self, email):
        user = User.query.filter_by(email=email).one_or_none()
        if user:
            return {'success': True}, 200
        return {'success': False}, 404


@user_management_ns.route('/deleteUser/<string:email>')
class DeleteUser(Resource):

    method_decorators = [jwt_required()]

    @user_management_ns.doc(security='jsonWebToken')
    @user_management_ns.marshal_list_with(success_model)
    def delete(self, email):
        user = User.query.filter_by(email=email).one_or_none()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'success': True}, 200
        return {'success': False}, 404


@user_management_ns.route('/getStats')
class GetStats(Resource):

    method_decorators = [jwt_required()]

    @user_management_ns.doc(security='jsonWebToken')
    # @user_management_ns.marshal_list_with(success_model)
    def get(self):
        returned_stats = []
        stats = PatientStats.query.all()
        if stats:
            for stat in stats:
                exercise_name = Exercises.query.filter_by(
                    id=stat.exercise_id
                ).first().name

                patient_name_surname = Patient.query.filter_by(
                    id=stat.patient_id
                ).first().name + " " + Patient.query.filter_by(
                    id=stat.patient_id
                ).first().surname

                # Convertir 'date' a una cadena
                date_string = stat.date.strftime("%Y-%m-%d %H:%M:%S")

                returned_stats.append({
                    "patient": patient_name_surname,
                    "exercise_name": exercise_name,
                    "total_time": stat.total_time,
                    "average_series_time": stat.average_series_time,
                    "average_time_between_reps":
                        stat.average_time_between_reps,
                    "reps_per_series": stat.reps_per_series,
                    "date": date_string
                })

            return returned_stats, 200
        return {'success': False}, 404


@user_management_ns.route('/getPatientStats/<int:patient_id>')
class GetPatientStats(Resource):

    method_decorators = [jwt_required()]

    @user_management_ns.doc(security='jsonWebToken')
    # @user_management_ns.marshal_list_with(success_model)
    def get(self, patient_id):
        returned_stats = []
        stats = PatientStats.query.filter_by(patient_id=patient_id).all()
        if stats:
            for stat in stats:
                exercise_name = Exercises.query.filter_by(
                    id=stat.exercise_id
                ).first().name
                returned_stats.append({
                    "patient_id": stat.patient_id,
                    "exercise_name": exercise_name,
                    "total_time": stat.total_time,
                    "average_series_time": stat.average_series_time,
                    "average_time_between_reps":
                        stat.average_time_between_reps,
                    "reps_per_series": stat.reps_per_series,
                })

            return returned_stats, 200
        return {'success': False}, 404


@user_management_ns.route('/verifyValidationToken')
class VerifyValidationToken(Resource):

    @user_management_ns.marshal_list_with(success_model)
    def post(self):
        user = User.query.filter_by(
            email=user_management_ns.payload["email"]
        ).one_or_none()

        if user:
            if user.password_token == user_management_ns.payload[
                "validationToken"
            ]:
                return {'success': True}, 200

        return {'success': False}, 404


@user_management_ns.route('/changePasswordWithoutToken')
class ChangePasswordWithoutToken(Resource):

    @user_management_ns.expect(changePassword_input_model)
    @user_management_ns.marshal_list_with(error_with_name_model)
    def put(self):
        user = User.query.filter_by(
            email=user_management_ns.payload["email"]
        ).one_or_none()

        if user:
            newPassword = generate_password_hash(
                user_management_ns.payload["newPassword"]
            )

            if check_password_hash(
                user.password_token, user_management_ns.payload["newPassword"]
            ):
                return {
                    'msg': '¡La contraseña anterior y nueva son iguales!'
                }, 304

            user.password_token = newPassword
            db.session.commit()
            return {'msg': 'Password changed successfully'}, 201
        return {
            'msg': 'There is not a user registered with the email provided'
        }, 404
