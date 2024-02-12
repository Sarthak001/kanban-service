import hashlib
from flask import request, Response, json, Blueprint
from src.models.password_reset_model import PasswordReset
from src.models.user_model import User
from src.models.user_role_model import UserRole
from src.models.otp_model import Otp
from src.models.board_model import Board
from src.models.task_model import Task
from src import bcrypt, db, config
from src.models.verification_model import UserVerification
from src.utils import otp_service, mail_service
import base64
import jwt
import os


task = Blueprint("task", __name__)

# route for gettask  api/v1/task/gettask
@task.route('/gettask',methods = ['GET'])
@task.route('/gettask/<int:id>',methods = ['GET'])
def get_task(id = None):
    pass


# route for createtask  api/v1/task/createtask
@task.route('/createtask',methods = ['POST'])
def create_task():
    try:
        data = request.json
        task_obj = Task(
            task_name = data['task_name'],
            board_id_fk = int(data['board_id_fk']),
            board_list_fk = int(data['board_list_fk'])
        )
        db.session.add(task_obj)
        db.session.commit()
        return Response(
                        json.dumps(
                            {
                                "status": "Sucess",
                                "error": None,
                                "data": {
                                    "message": f"Successfuly created task!!"
                            }
                        }),
                        status=200,
                        mimetype="application/json"
                        )
    except Exception as e:
        return Response(
                    json.dumps(
                        {
                            "status": "failed",
                            "error": None,
                            "data": {
                                "message": f"Internal Server Error!!"
                            }
                        }),
                    status=500,
                    mimetype="application/json"
                )