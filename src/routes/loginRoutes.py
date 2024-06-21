from src.models.api_models import (
    user_register_model, login_model, logged_model,
    logout_model, passwordRecovery_model, success_model
)
from src.models.models import User
from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import db
from flask_mail import Message
from src.extensions import mail

login_ns = Namespace('api/Sign')


@login_ns.route('/Register')
class RegisterUser(Resource):
    @login_ns.expect(user_register_model)
    @login_ns.marshal_with(user_register_model)
    def post(self):

        user = User(
            name=login_ns.payload['name'],
            email=login_ns.payload['email'],
            password_token=generate_password_hash(
                login_ns.payload['password']
            )
        )

        db.session.add(user)
        db.session.commit()
        return user, 201


@login_ns.route('/Login')
class LoginUser(Resource):
    @login_ns.expect(login_model)
    @login_ns.marshal_with(logged_model)
    def post(self):
        user = User.query.filter_by(email=login_ns.payload['email']).first()

        if not user:
            return {'message': 'User not found'}, 404
        if not check_password_hash(
            user.password_token, login_ns.payload['password']
        ):
            return {'message': 'Password does not match'}, 401

        user.access_token = create_access_token(user)
        db.session.commit()
        return user, 201


@login_ns.route('/Logout')
class LogoutUser(Resource):
    method_decorators = [jwt_required()]

    @login_ns.doc(security='jsonWebToken')
    @login_ns.expect(logout_model)
    @login_ns.marshal_with(logged_model)
    def post(self):
        user = User.query.filter_by(email=login_ns.payload['email']).first()
        user.access_token = None
        db.session.commit()
        return user, 201


"""
@login_ns.route('/RefreshJWToken')
class RefreshJWToken(Resource):
    method_decorators = [jwt_required()]

    @login_ns.doc(security='jsonWebToken')
    @login_ns.marshal_with(logged_model)
    def post(self):
        user = User.query.filter_by(email=login_ns.payload['email']).first()
        user.access_token = create_access_token(user)
        db.session.commit()
        return user, 201
"""


@login_ns.route('/getAccessToken/<string:email>')
class GetAccessToken(Resource):
    method_decorators = [jwt_required()]

    @login_ns.doc(security='jsonWebToken')
    @login_ns.marshal_with(logged_model)
    def get(self, email):
        user = User.query.filter_by(email=email).first()
        return user, 201


@login_ns.route('/passwordRecovery')
class PasswordRecovery(Resource):

    @login_ns.expect(passwordRecovery_model)
    @login_ns.marshal_list_with(success_model)
    def post(self):
        user = User.query.filter_by(
                email=login_ns.payload["email"]
            ).one_or_none()
        if user:
            msg = Message('Password Recovery',
                          sender='platform-support@example.com',
                          recipients=[user.email])
            url = 'http://localhost:5173/activateAccount/true'
            body = f'''
            Hola usuario, este es el token de validación que va a necesitar en
             el cambio de contraseña: {user.password_token}\n\n
            Por favor, acceda al siguiente link de cambio
             de contraseña para completar el proceso:\n\n{url}\n
            '''
            msg.body = body
            mail.send(msg)

            return {'success': True}
        else:
            return {'success': False}
