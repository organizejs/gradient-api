import os
from flask import Flask
from flask_restful import Resource, Api 
from flask_migrate import Migrate
from config import app_config
from .db import db
from .ma import ma
from .jwt import jwt
from .models import UserModel
from .views import main_bp
from .resources import (
  User, UserList, GoogleRedirect, GoogleRegisterAuthorized, 
  GoogleLoginAuthorized
)


def create_app(environment=None):
  app = Flask(__name__)
  api = Api(app)

  # get environment if not declared 
  environment = os.getenv("FLASK_ENV") \
    if environment is None else environment

  # load config based on specified environment
  app.config.from_object(app_config[environment])

  # start db
  db.init_app(app)

  # start marshmallow
  ma.init_app(app)

  # start jwt
  jwt.init_app(app)

  # load all models
  with app.app_context():
    db.configure_mappers()
    db.create_all()

  # add resources
  api.add_resource(UserList, '/users')
  api.add_resource(User, '/users/<int:user_id>')
  api.add_resource(GoogleRedirect, '/google/redirect')
  api.add_resource(GoogleRegisterAuthorized, '/google/register/authorized')
  api.add_resource(GoogleLoginAuthorized, '/google/login/authorized')

  # add blueprints
  app.register_blueprint(main_bp)

  return app

