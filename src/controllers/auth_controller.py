from flask import request, Response, json, Blueprint, current_app
from src import bcrypt, config
from src.utils import mail_service
from src.repositories import user_repository,verification_repository
from datetime import datetime
import base64
import jwt
import os
import threading
from src.middlewares.user_info import capture_user_info
import hashlib
from sqlalchemy import exc


# user controller blueprint to be registered with api blueprint
auth = Blueprint("auth", __name__)

# route for signup api/v1/auth/signup
@auth.route('/signup', methods=["POST"])
def handle_signup():
    try:
        data = request.json
        if "first_name" in data and "last_name" in data and "email" in data and "password" in data:
            user = user_repository.get_user_by_email(data["email"])
            if user:
                return Response(response=json.dumps({"status": "failed", "message": "User already exists"}), status=200,
                                mimetype="application/json")
            else:
                role = user_repository.get_user_role()
                user_obj = user_repository.create_user(role,data["first_name"],data["last_name"],data["email"],data["password"])

                print(user_obj.email)
                token_hash = hashlib.md5(f"{user_obj.email}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".encode('utf-8')).hexdigest()
                verification = verification_repository.create_verification(user_obj.user_id,token_hash)
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
            
    except exc.SQLAlchemyError as e:
        current_app.logger.error("ERROR OCCURED DURING DB OPERATION")
        return Response(json.dumps({
            "status": "failed",
            "error": "error occured during DB Operation ",
            "data": None
        }),
            status=500,
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
        db_res = verification_repository.get_verification(email,token)
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
            user_obj = user_repository.get_user_by_email(email)
            user_repository.update_user_active(user_obj)
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
        
    except exc.SQLAlchemyError as e:
        current_app.logger.error("ERROR OCCURED DURING DB OPERATION")
        return Response(json.dumps({
            "status": "failed",
            "error": "error occured during DB Operation ",
            "data": None
        }),
            status=500,
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
@capture_user_info
def handle_signin():
    try:
        current_app.logger.info("asdsadasd")
        data = request.json
        if "email" and "password" in data:
            user = user_repository.get_user_by_email(data["email"])
            if user and user.is_active:
                # checking for password match
                if bcrypt.check_password_hash(user.passwd, data["password"]):
                    # generating otp if password matched
                    one_time_code = verification_repository.create_otp(user)
                    # sending mail for otp verification
                    otp = " ".join(one_time_code)
                    mail_data = {
                        "recipient": user.email,
                        "otp": otp,
                        "user_info" : request.user_info
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
                        status=401,
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
                    status=401,
                    mimetype="application/json"
                )

    except exc.SQLAlchemyError as e:
        current_app.logger.error("ERROR OCCURED DURING DB OPERATION")
        return Response(json.dumps({
            "status": "failed",
            "error": "error occured during DB Operation ",
            "data": None
        }),
            status=500,
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
@auth.route('/verifysignin', methods=["POST"])
def handle_verifysignin():
    try:
        data = request.json
        #email = request.args.get('email')
        #otp = int(request.args.get('otp'))
        db_res = verification_repository.get_otp(data["email"],int(data["otp"]))
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
            if int(data["otp"]) == db_res[1]:
                user_obj = user_repository.get_user_by_email(data["email"])
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
        
    except exc.SQLAlchemyError as e:
        print(e)
        current_app.logger.error("ERROR OCCURED DURING DB OPERATION")
        return Response(json.dumps({
            "status": "failed",
            "error": "error occured during DB Operation ",
            "data": None
        }),
            status=500,
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


@auth.route('/forgotpassword', methods=["GET"])
def handle_forgotpassword2():
    try:
        req_email = request.args.get("email")
        user = user_repository.get_user_by_email(req_email)
        if user:
            verification_repository.create_password(user)
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
        
    except exc.SQLAlchemyError as e:
        current_app.logger.error("ERROR OCCURED DURING DB OPERATION")
        return Response(json.dumps({
            "status": "failed",
            "error": "error occured during DB Operation ",
            "data": None
        }),
            status=500,
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
            db_res = verification_repository.get_password_reset(data["email"],token)

            if db_res[0] and db_res[1] <= datetime.now() and not db_res[2]:
                user = user_repository.get_user_by_email(data["email"])
                updated_data =user_repository.update_user_password(user, data["password"])
                return Response(
                    json.dumps({}),
                    status=200,
                    mimetype="application/json"
                )
            
    except exc.SQLAlchemyError as e:
        current_app.logger.error("ERROR OCCURED DURING DB OPERATION")
        return Response(json.dumps({
            "status": "failed",
            "error": "error occured during DB Operation ",
            "data": None
        }),
            status=500,
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
        user = user_repository.get_user_by_email(email)
        if user:
            if operation == "verification" and not user.is_active:
                token_hash = hashlib.md5(f"{user.email}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".encode('utf-8')).hexdigest()
                verification = verification_repository.create_verification(user.user_id,token_hash)
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
                one_time_code = verification_repository.create_otp(user)
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
            
    except exc.SQLAlchemyError as e:
        current_app.logger.error("ERROR OCCURED DURING DB OPERATION")
        return Response(json.dumps({
            "status": "failed",
            "error": "error occured during DB Operation ",
            "data": None
        }),
            status=500,
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
