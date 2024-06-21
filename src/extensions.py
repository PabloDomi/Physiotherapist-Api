from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_mail import Mail

###
#
#           INSTANCIACIONES DE "Api" DE FLASK RESTX
#                              "db" DE SQLALCHEMY
#                              "jwt" DE FLASK-JWT-EXTENDED
#                              "migration" DE FLASK-MIGRATION
#
###

api = Api()
db = SQLAlchemy()
jwt = JWTManager()
migration = Migrate()
mail = Mail()
