from flask import request, Response, json, Blueprint,current_app
from src.repositories import task_repository
from sqlalchemy import exc 



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
        task_repository.create_task(data['task_name'],int(data['board_id_fk']), int(data['board_list_fk']))
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