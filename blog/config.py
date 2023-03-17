import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY') or 'secret'

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') \
                          or f'sqlite:///{os.getenv("PWD")}/blog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') \
                                 or False

FLASK_ADMIN_SWATCH = 'cosmo'

OPENAPI_URL_PREFIX = '/api/swagger'
OPENAPI_SWAGGER_UI_PATH = '/'
OPENAPI_SWAGGER_UI_VERSION = '3.22.0'
