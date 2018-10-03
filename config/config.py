import os


class Config(object):
  '''
  Parent configuration class
  '''
  DEBUG = False
  CSRF_ENABLED = True
  SECRET = os.getenv("SECRET")
  SECRET_KEY = os.getenv("SECRET")
  JWT_SECRET_KEY = os.getenv("JWT_SECRET")
  SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  ENV = os.getenv("FLASK_ENV")
  GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
  GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")


class DevelopmentConfig(Config):
  '''
  Configuration for Development
  '''
  DEBUG = True
  ENV = "development"


class TestingConfig(Config):
  '''
  Configuration for Testing, with a separate test database
  '''
  TESTING = True
  SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
  DEBUG = True
  ENV = "testing"


class StagingConfig(Config):
  '''
  Configuration for Staging
  '''
  DEBUG = True
  ENV = "staging"


class ProductionConfig(Config):
  '''
  Configuration for Production
  '''
  DEBUG = False
  TESTING = False
  ENV = "production"


'''
The keys are the possible 'environments' to select from
Select your 'environment' to get the appropriate config
'''
app_config = {
  "development": DevelopmentConfig,
  "testing": TestingConfig,
  "staging": StagingConfig,
  "production": ProductionConfig
}
  
