from flask import Flask
from flask_mail import Mail
import os
from src.config.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# for password hashing
from flask_bcrypt import Bcrypt

# loading environment variables
load_dotenv()

# declaring flask application
service = Flask(__name__, static_url_path='/static')

# calling the service configuration based on the env
if os.environ.get("ENV") == "PROD":
    config = Config().production_config
else:
    config = Config().dev_config

# making our application to use dev env
service.env = config.ENV

# load the secret key defined in the .env file
service.secret_key = os.environ.get("SECRET_KEY")
bcrypt = Bcrypt(service)

# Config Flask-Mail
service.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
service.config['MAIL_PORT'] = 465
service.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
service.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
service.config['MAIL_USE_TLS'] = False
service.config['MAIL_USE_SSL'] = True
mail = Mail(service)

# Path for our local sql lite database
service.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")

# To specify to track modifications of objects and emit signals
service.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

# sql alchemy instance
db = SQLAlchemy(service)

# Flask Migrate instance to handle migrations
migrate = Migrate(service, db)

# import api blueprint to register it with app
from src.routes import api

service.register_blueprint(api, url_prefix="/api/v1")

# import models under models/__init__.py to let the migrate tool know
from src.models.user_model import User
from src.models.user_role_model import UserRole
from src.models.otp_model import Otp


