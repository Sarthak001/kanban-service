import hashlib
from flask import request, Response, json, Blueprint
from src.models.user_model import User
from src.models.board_model import Board
from src import bcrypt, db, config
from src.utils import otp_service, mail_service,user_service
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
        decoded_data = user_service.get_CurrentUser()
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


# route for getbaord  api/v1/board/getboard/<id : optional>
@board.route('/getboard',methods = ['GET'])
@board.route('/getboard/<int:id>',methods = ['GET'])
def get_board(id = None):
    try:
        data = user_service.get_CurrentUser()
        # print(id)
        if id == None:
            db_res = db.session.query(Board).filter(Board.board_owner_fk == int(data['user_id'])).all()
            board_details= []
            for i in db_res:
                board_details.append([json.dumps(i.board_id),json.dumps(i.board_name),json.dumps(i.created_at)])
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
        else :
            db_res = db.session.query(Board).filter(Board.board_id == id).first()
            if db_res:
                return Response(
                        json.dumps(
                            {
                                "status": "sucess",
                                "error": None,
                                "data": {
                                    "message": f"Boards Details!!",
                                    "boards_details" : {
                                        "Created At" : db_res.created_at,
                                        "Board Owner" : db_res.board_owner_fk,
                                        "Board Name" : db_res.board_name,
                                        "Id" : db_res.board_id,
                                        
                                    }
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
                                    "message": f"No such board exists!!"
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
        

# route for updateboard  api/v1/board/updateboard/<id>
@board.route('/updateboard/<int:id>',methods = ['GET','PATCH'])
def update_board(id):
    try:
        headers = request.args.items()
        d = {}
        for i,j in headers:
            d[i] = j
        data = user_service.get_CurrentUser()
        board_obj = Board.query.filter_by(board_id=id).first()
        if board_obj and board_obj.board_owner_fk == int(data['user_id']):
            for key, value in d.items():
                if hasattr(Board,key):
                    setattr(board_obj,key,value)
            db.session.commit()
            return Response(
                            json.dumps(
                                {
                                    "status": "sucess",
                                    "error": None,
                                    "data": {
                                        "message": f"Board Successfully Updated!!"
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
                                        "message": f"Board Id does not exist or you are not the Owner of the Board!!"
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
        

# route for deleteboard  api/v1/board/deleteboard/<id>
@board.route('/deleteboard/<int:id>',methods = ['DELETE'])
def delete_board(id):
    try:
        data = user_service.get_CurrentUser()
        board_obj = Board.query.filter_by(board_id=id).first()
        print(board_obj)
        if board_obj and board_obj.board_owner_fk == int(data['user_id']):
            db.session.delete(board_obj)
            db.session.commit()
            return Response(
                            json.dumps(
                                {
                                    "status": "sucess",
                                    "error": None,
                                    "data": {
                                        "message": f"Board Deleted Successfully !!"
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
                                        "message": f"Board Id does not exist or you are not the Owner of the Board!!"
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