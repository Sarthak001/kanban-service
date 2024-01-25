from flask import request, Response, json, Blueprint
from src.models.user_model import User
from src.models.user_role_model import UserRole
from src.models.otp_model import Otp
from src import bcrypt, db,config
from src.utils import otp_service
from src.utils import mail_service
from datetime import datetime
import base64 

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
                return Response(response=json.dumps({'status': "failed", "message": "User already exists"}), status=200, mimetype="application/json")
            else:
                role = db.session.query(UserRole.role_id).filter(UserRole.role_name == "normal user").first()
                user_obj = User(
                    role_id_fk=role[0],
                    user_name=data['first_name'] +
                    data['last_name'] + str(randint(10, 99)),
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    passwd=bcrypt.generate_password_hash(
                        data['password']).decode('utf-8'),
                    is_active=False,
                )
                db.session.add(user_obj)
                db.session.commit()

                one_time_code = otp_service.GenerateOtp()
                otp_obj = Otp(
                    user_id_fk = user_obj.user_id,
                    otp = one_time_code
                )
                db.session.add(otp_obj)
                db.session.commit()

                base64_bytes = (base64.b64encode((f"{user_obj.email}:{one_time_code}").encode("UTF-8"))).decode("UTF-8")
                mailData = {"host":config.HOST,
                            "recipient" : user_obj.email, 
                            "bodydata":base64_bytes
                           }
                mail_service.SendMail("email verification",mailData)
                return Response(
                    json.dumps(
                        {
                            "status": "success",
                            "error": None,
                            "data": {
                                "message": f"User created successfully. Please verfiy your email id. Verification code has been sent to Email:{user_obj.email}"
                            }
                        }),
                    status=201,
                    mimetype="application/json"
                )
    except Exception as e:
        return Response(
            json.dumps({
                "status": "failed",
                "error": "Internal server error",
                "data": None
            }),
            status=500,
            mimetype="application/json"
        )


@auth.route('/verifyEmail',methods = ["GET"])
def handle_verifyEmail():
    try:
        token = (base64.b64decode((request.args.get('token')).encode("UTF-8"))).decode("UTF-8")
        email, otp, *_ = token.split(":")
        otp = int(otp)
        db_res = db.session.query(User.email,Otp.otp,Otp.expire_in).join(User.otp).filter(User.email==email,Otp.otp==int(otp)).order_by(Otp.id.desc()).first()
        if db_res:
            if db_res[2] <= datetime.now():
                return Response(
                        json.dumps(
                            {
                                "status": "failed",
                                "error": None,
                                "data": {
                                    "message": f"Verifcation Link expired"
                                }
                            }),
                        status=200,
                        mimetype="application/json"
                    )   
            if otp == db_res[1]:
                user_obj=User.query.filter_by(email=email).first()
                user_obj.is_active = True
                db.session.commit()
                return Response(
                        json.dumps(
                            {
                                "status": "success",
                                "error": None,
                                "data": {
                                    "message": f"User email verified successfully"
                                }
                            }),
                        status=200,
                        mimetype="application/json"
                    )   
            return Response(
                json.dumps({
                    "status": "failed",
                    "error": "Failed to verify user email",
                    "data": None
                }),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                json.dumps({
                    "status": "failed",
                    "error": "user is not registered",
                    "data": None
                }),
                status=200,
                mimetype="application/json"
            )
    except Exception as e:
        return Response(json.dumps({
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
    try:
        data = request.json
        if "email" and "password" in data:
            user = User.query.filter_by(email=data["email"]).first()
            if user and user.is_active == True:
                # cheching for password match
                if bcrypt.check_password_hash(user.passwd, data["password"]):
                    # generating otp if password matched
                    one_time_code = otp_service.GenerateOtp()
                    otp_obj = Otp(
                        user_id_fk = user.user_id,
                        otp = one_time_code
                    )
                    db.session.add(otp_obj)
                    db.session.commit()
                    # sending mail for otp verification
                    base64_bytes = (base64.b64encode((f"{user.email}:{one_time_code}").encode("UTF-8"))).decode("UTF-8")
                    mailData = {"host":config.HOST,
                            "recipient" : user.email, 
                            "bodydata":base64_bytes
                           }
                    mail_service.SendMail("user login verification",mailData)
                    return Response(
                    json.dumps(
                        {
                            "status": "success",
                            "error": None,
                            "data": {
                                "message": f"Please enter the One- Time Verification code sent to Email:{user.email}"
                            }
                        }),
                    status=201,
                    mimetype="application/json"
                )
                # if password did not matched
                else:
                    return Response(
                        json.dumps(
                            {
                                "status": "failed",
                                "error": None,
                                "data": {
                                    "message": f"Wrong Password!"
                                }
                            }),
                        status=200,
                        mimetype="application/json"
                    )
            else:
                # user does not exists
                return Response(
                        json.dumps(
                            {
                                "status": "failed",
                                "error": None,
                                "data": {
                                    "message": f"User does not exists or either you did not verified your email. "
                                }
                            }),
                        status=200,
                        mimetype="application/json"
                    )
        
    except Exception as e:
        print(e)
        return Response(json.dumps({
                    "status": "failed",
                    "error": "Internal server error",
                    "data": None
                }),
                status=500,
                mimetype="application/json"
            )


@auth.route('/verifyLogin',methods = ["GET"])
def handle_verifyLogin():
    try:
        email = request.args.get('email')
        otp = request.args.get('otp')
        # email, otp, *_ = token.split(":")
        otp = int(otp)
        db_res = db.session.query(User.email,Otp.otp,Otp.expire_in).join(User.otp).filter(User.email==email,Otp.otp==int(otp)).order_by(Otp.id.desc()).first()
        if db_res:
            if db_res[2] <= datetime.now():
                return Response(
                        json.dumps(
                            {
                                "status": "failed",
                                "error": None,
                                "data": {
                                    "message": f"OTP expired"
                                }
                            }),
                        status=200,
                        mimetype="application/json"
                    )   
            if otp == db_res[1]:
                user_obj=User.query.filter_by(email=email).first()
                # create token
                payload = {
                        'user_id': str(user_obj.user_id),
                        'role': user_obj.role_id_fk,
                        'firstname': user_obj.first_name,
                        'lastname': user_obj.last_name,
                        'email': user_obj.email,
                        }
                jwttoken = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')

                return Response(
                        json.dumps(
                            {
                                "status": "success",
                                "error": None,
                                "data": {
                                    "token" : jwttoken,
                                    "message": f"Login successfull!!"
                                }
                            }),
                        status=200,
                        mimetype="application/json"
                    )   
            return Response(
                json.dumps({
                    "status": "failed",
                    "error": "Failed to verify the OTP",
                    "data": None
                }),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                json.dumps({
                    "status": "failed",
                    "error": "User is not registered",
                    "data": None
                }),
                status=200,
                mimetype="application/json"
            )
    except Exception as e:
        print(e)
        return Response(json.dumps({
                    "status": "failed",
                    "error": "Internal server error",
                    "data": None
                }),
                status=500,
                mimetype="application/json"
            )



@auth.route('/forgotpassword', methods=["GET", "POST"])
def handle_forgotpassword():
    pass


@auth.route('/resendotp', methods=["GET"])
def handle_resendotp():
    pass
