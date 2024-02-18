from flask import request, Response, json, Blueprint,current_app
from src.middlewares.jwt_auth import jwt_required
from src.repositories import user_repository,board_repository
from sqlalchemy import exc



board = Blueprint("board", __name__)

# route for createboard  api/v1/board/createboard
@board.route('/createboard',methods = ['GET','POST'])
@jwt_required
def create_board():
    try:
        boardname = request.args.get("board_name")
        decoded_data = request.current_user
        db_res = user_repository.get_user_by_email(decoded_data['email'])
        if db_res:
            if not db_res.is_active:
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
                board_repository.create_board(boardname,db_res.user_id)
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


# route for getbaord  api/v1/board/getboard/<id : optional>
@board.route('/getboard',methods = ['GET'])
@board.route('/getboard/<int:id>',methods = ['GET'])
@jwt_required
def get_board(id = None):
    try:
        data = request.current_user
        # print(id)
        if id == None:
            db_res = board_repository.get_board_owned(int(data['user_id']))
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
            db_res = board_repository.get_board_by_id(id)
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
                    json.dumps(
                        {
                            "status": "Failed",
                            "error": "Internal Server Error",
                            "data": None
                        }),
                    status=500,
                    mimetype="application/json"
                )
        

# route for getboardmembers api/v1/board/boardmembers/<id>
@board.route('/boardmembers/<int:id>',methods = ['GET'])
@jwt_required
def get_board_members(id):
    try:
        data = request.current_user
        db_res = board_repository.get_board_members(int(id))
        user_details = user_repository.get_user_by_id(int(db_res[0].member_fk))
        return Response(
                        json.dumps(
                            {
                                "status": "sucess",
                                "error": None,
                                "data": {
                                    "message": f"Boards Members Details!!",
                                    "boards__member_details" : {
                                        "Created At" : user_details.created_at,
                                        "Is Active" : user_details.is_active,
                                        "User Name" : user_details.user_name,
                                        "Id" : user_details.user_id,
                                        
                                    }
                                }
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
@jwt_required
def update_board(id):
    try:
        headers = request.args.items()
        d = {}
        for i,j in headers:
            d[i] = j
        data = request.current_user
        board_obj = board_repository.get_board_by_id(id)
        if board_obj and board_obj.board_owner_fk == int(data['user_id']):
            board_repository.update_board(d,board_obj)
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
@jwt_required
def delete_board(id):
    try:
        data = request.current_user
        board_obj = board_repository.get_board_by_id(id)
        if board_obj and board_obj.board_owner_fk == int(data['user_id']):
            board_repository.delete_board(board_obj)
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
                    json.dumps(
                        {
                            "status": "Failed",
                            "error": "Internal Server Error",
                            "data": None
                        }),
                    status=500,
                    mimetype="application/json"
                )