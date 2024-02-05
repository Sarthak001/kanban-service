import hashlib
from flask import request, Response, json, Blueprint
from src.models.password_reset_model import PasswordReset
from src.models.user_model import User
from src.models.user_role_model import UserRole
from src.models.otp_model import Otp
from src.models.board_model import Board
from src import bcrypt, db, config
from src.models.verification_model import UserVerification
from src.utils import otp_service, mail_service,get_CurrentUser
from datetime import datetime
import base64
import jwt
import os



board = Blueprint("board", __name__)

# route for createboard  api/v1/board/createboard
@board.route('/createboard',methods = ['GET','POST'])
def create_board():
    try:
        boardname = request.args.get("board_name")
        decoded_data = get_CurrentUser.get_CurrentUser()
        print(decoded_data)
        db_res = db.session.query(User.user_id,User.is_active).filter(User.email == decoded_data['email']).first()
        if db_res:
            if not db_res[1]:
                return Response(
                    json.dumps(
                        {
                            "status": "failed",
                            "error": None,
                            "data": {
                                "message": f"Please verify your email first!!"
                            }
                        }),
                    status=200,
                    mimetype="application/json"
                )
            else:
                board_obj = Board(
                    board_name  = boardname,
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
                                "message": f"User does not exits or has not verified the email!!"
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


# route for createboard  api/v1/board/getboard
@board.route('/getboard',methods = ['GET'])
def get_board():
    try:
        data = get_CurrentUser.get_CurrentUser()
        db_res = db.session.query(Board.board_name,Board.created_at).filter(Board.board_owner_fk == data['user_id']).all()
        board_details= []
        for i in db_res:
            board_details.append([json.dumps(i.board_name),json.dumps(i.created_at)])
        if db_res:
            return Response(
                    json.dumps(
                        {
                            "status": "sucess",
                            "error": None,
                            "data": {
                                "message": f"Boards owned by you:!!",
                                "boards_details" : board_details
                            }
                        }),
                    status=200,
                    mimetype="application/json"
                )
        else:
            return Response(
                    json.dumps(
                        {
                            "status": "sucess",
                            "error": None,
                            "data": {
                                "message": f"No Boards owned by you!!"
                            }
                        }),
                    status=200,
                    mimetype="application/json"
                )
    except Exception as e:
        print(e)
        return Response(
                    json.dumps(
                        {
                            "status": "Failed",
                            "error": "Internal Server Error",
                            "data": None
                        }),
                    status=500,
                    mimetype="application/json"
                )
        


