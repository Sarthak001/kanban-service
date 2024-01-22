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
    user_obj = User.query.filter_by(user_id=1).first()
    otp_obj = Otp(
        user_id_fk = user_obj.user_id,
        otp = 567834
    )
    db.session.add(otp_obj)
    db.session.commit()
    return "hello world"


# route for login api/users/signin


@auth.route('/signin', methods=["POST"])
def handle_login():
    return
