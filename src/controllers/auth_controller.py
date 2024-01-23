from flask import request, Response, json, Blueprint
from src.models.user_model import User
from src.models.user_role_model import UserRole
from src.models.otp_model import Otp
from src import bcrypt, db
from datetime import datetime
import jwt
import os
from random import randint

# user controller blueprint to be registered with api blueprint
auth = Blueprint("auth", __name__)

# route for signup api/users/signup


@auth.route('/signup', methods=["GET"])
def handle_signup():
    data = request.json
    if "first_name" in data and "last_name" in data and "email" in data and "password" in data:
        user = User.query.filter_by(email=data["email"]).first()
        if user:
            return Response(response=json.dumps({'status': "failed", "message": "User already exists"}))
        else:
            role = UserRole.query.filter_by(role_name="normal user").first()
            # print(role.role_id)
            user_obj = User(
                role_id_fk=role.role_id,
                user_name=data['first_name'] +
                data['last_name'] + str(randint(10, 99)),
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                passwd=bcrypt.generate_password_hash(
                    str(data['password'])).decode('utf-8'),
                is_active=True,
                last_login=datetime.now()
            )
            db.session.add(user_obj)
            db.session.commit()

            payload = {
                'firstname': user_obj.first_name,
                'lastname': user_obj.last_name,
                'username': user_obj.user_name,
                'email': user_obj.email,
            }
            token = jwt.encode(payload=payload, key=os.getenv(
                'SECRET_KEY'), algorithm='HS256')

            return Response(response=json.dumps({"status": "Sucess", "Message": f"User successfully created for {data['first_name']} as {user_obj.user_name}", "token": token}))
    else:
        return Response(response=json.dumps({"status": "failed", "message": "Enter correct details"}))


# route for login api/users/signin


@auth.route('/signin', methods=["POST"])
def handle_login():
    return


@auth.route('forgotpassword', methods=["GET", "POST"])
def handle_forgotpassword():
    pass


@auth.route('resendotp', methods=["GET"])
def handle_resendotp():
    pass
