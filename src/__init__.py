from dotenv import load_dotenv
from flask import Flask
from src.config.config import Config
from .extensions import api, db, jwt, migration
from flask_cors import CORS
from src.models.models import User
from src.routes.routes import ns


def create_app():

    load_dotenv()

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)
    api.init_app(app)
    jwt.init_app(app)
    migration.init_app(app, db)
    api.add_namespace(ns)

    return app


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
