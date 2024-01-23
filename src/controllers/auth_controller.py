from flask import request, Response, json, Blueprint
from src.models.user_model import User
from src.models.user_role_model import UserRole
from src.models.otp_model import Otp
from src import bcrypt, db
from datetime import datetime
import jwt
import os

# user controller blueprint to be registered with api blueprint
auth = Blueprint("auth", __name__)

# route for signup api/users/signup


@auth.route('/signup', methods=["GET"])
def handle_signup():
    return "hello world"


# route for login api/users/signin


@auth.route('/signin', methods=["POST"])
def handle_login():
    return


@auth.route('forgotpassword',methods=["GET","POST"])
def handle_forgotpassword():
    pass


@auth.route('resendotp',methods=["GET"])
def handle_resendotp():
    pass