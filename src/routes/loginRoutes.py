from src.models.api_models import (
    user_register_model, login_model, logged_model
)
from src.models.models import User
from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from src.extensions import db

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
