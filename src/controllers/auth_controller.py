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

# route for signup api/v1/auth/signup
@auth.route('/signup', methods=["POST"])
def handle_signup():
    try:
        data = request.json
        if "first_name" in data and "last_name" in data and "email" in data and "password" in data:
            user = User.query.filter_by(email=data["email"]).first()
            if user:
                return Response(response=json.dumps({'status': "failed", "message": "User already exists"}),status=200,mimetype="application/json")
            else:
                role = UserRole.query.filter_by(role_name="normal user").first()
                user_obj = User(
                    role_id_fk=role.role_id,
                    user_name=data['first_name'] + data['last_name'] + str(randint(10, 99)),
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    passwd=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
                    is_active=False,
                    last_login=datetime.now()
                )
                db.session.add(user_obj)
                db.session.commit()
                return Response(
                    json.dumps(
                        {
                            "status" : "success",
                            "error" : None,
                            "data" : {
                                "message" : f"User created successfully. Please verfiy your email id. Verification link has been sent to Email:{user_obj.email}"
                            }
                        }),
                    status=201,
                    mimetype="application/json"
                    )
    except Exception as e:
        print(e)
        return Response(
            json.dumps({
                "status": "failed",
                "error": "Internal server error",
                "data": None
            }),
            status=500,
            mimetype="application/json"
        )






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
