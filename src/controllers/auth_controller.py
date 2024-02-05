import hashlib

from flask import request, Response, json, Blueprint

from src.models.password_reset_model import PasswordReset
from src.models.user_model import User
from src.models.user_role_model import UserRole
from src.models.otp_model import Otp
from src import bcrypt, db, config
from src.models.verification_model import UserVerification
from src.utils import otp_service, mail_service
from datetime import datetime
import base64
import jwt
import os
from random import randint
import threading


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
                return Response(response=json.dumps({"status": "failed", "message": "User already exists"}), status=200,
                                mimetype="application/json")
            else:
                role = db.session.query(UserRole.role_id).filter(UserRole.role_name == "normal user").first()
                user_obj = User(
                    role_id_fk=role[0],
                    user_name=data["first_name"] + data["last_name"] + str(randint(10, 99)),
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    email=data["email"],
                    passwd=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
                    is_active=False,
                )
                db.session.add(user_obj)
                db.session.commit()

                print(user_obj.email)
                token_hash = hashlib.md5(f"{user_obj.email}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".encode('utf-8')).hexdigest()

                verification = UserVerification(
                    user_id_fk=user_obj.user_id,
                    token=token_hash,
                    consumed=False
                )
                db.session.add(verification)
                db.session.commit()

                base64_bytes = (base64.b64encode(f"{user_obj.email}:{token_hash}".encode("UTF-8"))).decode("UTF-8")
                mail_data = {"host": config.HOST,
                             "recipient": user_obj.email,
                             "body-data": base64_bytes
                             }
                thread = threading.Thread(target=mail_service.send_mail, args=("email verification", mail_data))
                thread.start()
                return Response(
                    json.dumps(
                        {
                            "status": "success",
                            "error": None,
                            "data": {
                                "message": f"User created successfully. Please verify your email id. Verification "
                                           f"code has been sent to Email:{user_obj.email}"
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


# route for verifyemail api/v1/auth/verifyEmail
@auth.route('/verifyemail', methods=["GET"])
def handle_verifyemail():
    try:
        token = (base64.b64decode((request.args.get('token')).encode("UTF-8"))).decode("UTF-8")
        email, token, *_ = token.split(":")
        db_res = db.session.query(User.email, UserVerification.token, UserVerification.expire_in).join(
            User.verification).filter(User.email == email, UserVerification.token == token).order_by(
            UserVerification.id.desc()).first()
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
            user_obj = User.query.filter_by(email=email).first()
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


# route for signin api/v1/auth/signin
@auth.route('/signin', methods=["POST"])
def handle_signin():
    try:
        data = request.json
        if "email" and "password" in data:
            user = User.query.filter_by(email=data["email"]).first()
            if user and user.is_active:
                # checking for password match
                if bcrypt.check_password_hash(user.passwd, data["password"]):
                    # generating otp if password matched
                    one_time_code = str(otp_service.GenerateOtp())
                    otp_obj = Otp(
                        user_id_fk=user.user_id,
                        otp=one_time_code
                    )
                    db.session.add(otp_obj)
                    db.session.commit()
                    # sending mail for otp verification
                    otp = " ".join(one_time_code)
                    mail_data = {
                        "recipient": user.email,
                        "otp": otp
                    }
                    mail_service.send_mail("user login verification", mail_data)
                    return Response(
                        json.dumps(
                            {
                                "status": "success",
                                "error": None,
                                "data": {
                                    "message": f"Please enter the One - "
                                               f"Time Verification code sent to Email:{user.email}"
                                }
                            }),
                        status=200,
                        mimetype="application/json"
                    )
                # if password did not match
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


# route for verifysignin  api/v1/auth/verifysignin
@auth.route('/verifysignin', methods=["GET"])
def handle_verifysignin():
    try:
        email = request.args.get('email')
        otp = int(request.args.get('otp'))
        db_res = db.session.query(User.email, Otp.otp, Otp.expire_in) \
            .join(User.otp).filter(User.email == email, Otp.otp == otp) \
            .order_by(Otp.id.desc()).first()
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
                user_obj = User.query.filter_by(email=email).first()
                # create token
                payload = {
                    'user_id': str(user_obj.user_id),
                    'role': user_obj.role_id_fk,
                    'firstname': user_obj.first_name,
                    'lastname': user_obj.last_name,
                    'email': user_obj.email,
                }
                jwttoken = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
                return Response(
                    json.dumps(
                        {
                            "status": "success",
                            "error": None,
                            "data": {
                                "token": jwttoken,
                                "message": f"User signed in successfully!!"
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
        return Response(json.dumps({
            "status": "failed",
            "error": "Internal server error",
            "data": None
        }),
            status=500,
            mimetype="application/json"
        )


@auth.route('/forgotpassword', methods=["GET"])
def handle_forgotpassword2():
    try:
        req_email = request.args.get("email")
        user = User.query.filter_by(email=req_email).first()
        if user:
            passwd_obj = PasswordReset(
                user_id_fk=user.user_id,
                token=hashlib.md5(f"{user['email']}".encode('utf-8')).hexdigest(),
                consumed=False
            )
            db.session.add(passwd_obj)
            db.session.commit()
            return Response(
                json.dumps({}),
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

    except:
        return Response(json.dumps({
            "status": "failed",
            "error": "Internal server error",
            "data": None
        }),
            status=500,
            mimetype="application/json"
        )


# route for forgot password api/v1/auth/forgotpassword
@auth.route('/forgotpassword/<token>', methods=["PATCH"])
def handle_forgotpassword(token):
    try:
        data = request.json
        if "email" in data and "password" in data:

            db_res = db.session.query(User.is_active, PasswordReset.expire_in, PasswordReset.consumed).join(
                User.reset_pd).filter(
                User.email == data["email"], PasswordReset.token == token).order_by(PasswordReset.id.desc()).first()

            if db_res[0] and db_res[1] <= datetime.now() and not db_res[2]:
                user = User.query.filter_by(email=data["email"]).first()
                user.passwd = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                db.session.add(user)
                db.session.commit()
                return Response(
                    json.dumps({}),
                    status=200,
                    mimetype="application/json"
                )
    except:
        return Response(json.dumps({
            "status": "failed",
            "error": "Internal server error",
            "data": None
        }),
            status=500,
            mimetype="application/json"
        )


# route for resendotp api/v1/auth/resend/<operation>
@auth.route('/resend/<operation>', methods=["GET"])
def handle_resend(operation):
    try:
        email = request.args.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            if operation == "verification" and not user.is_active:
                token_hash = hashlib.md5(f"{user.email}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".encode('utf-8')).hexdigest()
                verification = UserVerification(
                    user_id_fk=user.user_id,
                    token=token_hash,
                    consumed=False
                )
                db.session.add(verification)
                db.session.commit()
                base64_bytes = (base64.b64encode(f"{user.email}:{token_hash}".encode("UTF-8"))).decode("UTF-8")
                mail_data = {"host": config.HOST,
                             "recipient": user.email,
                             "body-data": base64_bytes
                             }
                mail_service.send_mail("email verification", mail_data)
                return Response(
                    json.dumps({}),
                    status=200,
                    mimetype="application/json"
                )
            if operation == "otp":
                one_time_code = str(otp_service.GenerateOtp())
                otp_obj = Otp(
                    user_id_fk=user.user_id,
                    otp=one_time_code
                )
                db.session.add(otp_obj)
                db.session.commit()
                # sending mail for otp verification
                otp = " ".join(one_time_code)
                mail_data = {
                    "recipient": user.email,
                    "otp": otp
                }
                mail_service.send_mail("user login verification", mail_data)
                return Response(
                    json.dumps({}),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    json.dumps({}),
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
