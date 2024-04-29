from src.models.api_models import (
    success_model, changePassword_input_model
)
from src.models.models import User
from src.extensions import db
from werkzeug.security import generate_password_hash
from flask_restx import Resource, Namespace

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
