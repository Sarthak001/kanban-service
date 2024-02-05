import hashlib
from flask import request, Response, json, Blueprint
from src.models.password_reset_model import PasswordReset
from src.models.user_model import User
from src.models.user_role_model import UserRole
from src.models.otp_model import Otp
from src.models.board_model import Board
from src import bcrypt, db, config
from src.models.verification_model import UserVerification
from src.utils import otp_service, mail_service
from datetime import datetime
import base64
import jwt
import os



board = Blueprint("board", __name__)

# route for createboard  api/v1/board/createboard
@board.route('/createboard',methods = ['GET','POST'])
def create_board():
    try:
        
        headers = request.headers
        bearer = headers.get('Authorization')   # Bearer YourTokenHere
        token = bearer.split()[1]
        decoded_data = jwt.decode(jwt=token, key = os.getenv('SECRET_KEY'), algorithms=['HS256'])
        print(decoded_data['email'])
        db_res = db.session.query(User.user_id).filter(User.email == decoded_data['email']).first()
        if db_res:
            if db_res[0] <= datetime.now():
                return Response(
                    json.dumps(
                        {
                            "status": "failed",
                            "error": None,
                            "data": {
                                "message": f"Login expired.Please Login again!!"
                            }
                        }),
                    status=200,
                    mimetype="application/json"
                )
            else:
                board_obj = Board(
                    board_name  = "Sprint2",
                    board_owner_fk = db_res[0]
                )
                db.session.add(board_obj)
                db.session.commit()
                return Response(
                    json.dumps(
                        {
                            "status": "sucess",
                            "error": None,
                            "data": {
                                "message": f"Board created sucessfully!!"
                            }
                        }),
                    status=200,
                    mimetype="application/json"
                )
        else:
            return Response(
                    json.dumps(
                        {
                            "status": "failed",
                            "error": None,
                            "data": {
                                "message": f"db_res not found"
                            }
                        }),
                    status=200,
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

        


