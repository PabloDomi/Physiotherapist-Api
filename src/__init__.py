from dotenv import load_dotenv
from flask import Flask
from src.config.config import Config
from .extensions import api, db, jwt, migration
from flask_cors import CORS
from src.models.models import User
from src.routes.routes import ns
from src.routes.loginRoutes import login_ns
from src.routes.userManagementRoutes import user_management_ns
from src.routes.patientManagementRoutes import patient_management_ns
from src.routes.routineManagementRoutes import routine_management_ns


def create_app():

    load_dotenv()

    app = Flask(__name__)

    app.config.from_object(Config)

    # Instance of db
    db.init_app(app)

    # Enable CORS
    CORS(app)

    # Initialize the app with the api
    api.init_app(app)

    # Initialize the app with the jwt
    jwt.init_app(app)

    # Initialize the app with the migration
    migration.init_app(app, db)

    # Add the namespaces to the app
    api.add_namespace(ns)
    api.add_namespace(login_ns)
    api.add_namespace(user_management_ns)
    api.add_namespace(patient_management_ns)
    api.add_namespace(routine_management_ns)

    return app


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
