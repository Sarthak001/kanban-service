from flask import request, Response, json, Blueprint,current_app
from src.middlewares.jwt_auth import jwt_required
from src.repositories import task_repository
from sqlalchemy import exc 



task = Blueprint("task", __name__)

# route for gettask  api/v1/task/getboardtask
@task.route('/getboardtask/<int:id>',methods = ['GET'])
@jwt_required
def get_board_task(id = None):
    try:
        if id == None:
            return Response(json.dumps(
                            {
                                "status": "Sucess",
                                "error": None,
                                "data": {
                                    "message": f"Please mention Board ID!!"
                            }
                        }),
                        status=200,
                        mimetype="application/json"
                        )
        else:
            db_res = task_repository.get_task_by_board_id(id)
            if not db_res:
                return Response(json.dumps(
                            {
                                "status": "Sucess",
                                "error": None,
                                "data": {
                                    "message": f"No such Id exists!!"
                            }
                        }),
                        status=200,
                        mimetype="application/json"
                        )
            else:
                tasks = []
                for i in db_res:
                    tasks.append(
                        {'id': i.task_id,
                        'task_name' :i.task_name,
                        'assigned_to':i.assigned_to,
                        'board_list':i.board_list_fk,
                        'created_at':i.created_at,
                        'due_date':i.due_date})

                return Response(json.dumps(
                                {
                                    "status": "Sucess",
                                    "error": None,
                                    "data": tasks
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
                            "status": "failed",
                            "error": None,
                            "data": {
                                "message": f"Internal Server Error!!"
                            }
                        }),
                    status=500,
                    mimetype="application/json"
                )
    
@task.route('/assignedtome',methods = ['GET'])
@jwt_required
def get_tasks_asssigned():
    try:
        data = request.current_user
        db_res = task_repository.get_task_assigned_to_me(int(data['user_id']))
        if not db_res:
            return Response(json.dumps(
                            {
                                "status": "Sucess",
                                "error": None,
                                "data": {
                                    'message':'No task assigned to you!!'
                                }
                        }),
                        status=200,
                        mimetype="application/json"
                        )
        else:
            tasks = []
            for i in db_res:
                tasks.append({'id': i.task_id,
                        'task_name' :i.task_name,
                        'assigned_to':i.assigned_to,
                        'board_list':i.board_list_fk,
                        'created_at':i.created_at,
                        'due_date':i.due_date})
            
            return Response(json.dumps(
                            {
                                    "status": "Sucess",
                                    "error": None,
                                    "data": tasks
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
                            "status": "failed",
                            "error": None,
                            "data": {
                                "message": f"Internal Server Error!!"
                            }
                        }),
                    status=500,
                    mimetype="application/json"
                )
    
@task.route('/gettask/<int:id>',methods = ["GET"])    
@jwt_required
def get_task(id):
    try:
        db_res = task_repository.get_task_by_id(id)
        if not db_res:
            return Response(json.dumps(
                            {
                                "status": "Sucess",
                                "error": None,
                                "data": {
                                    "message": f"No such Id exists!!"
                            }
                        }),
                        status=200,
                        mimetype="application/json"
                        )
        else:
            task = [{
                                        'id': db_res[0].task_id,
                                        'task_name' :db_res[0].task_name,
                                        'assigned_to':db_res[0].assigned_to,
                                        'board_list':db_res[0].board_list_fk,
                                        'created_at':db_res[0].created_at,
                                        'due_date':db_res[0].due_date    
                                }]
            return Response(json.dumps(
                            {
                                "status": "Sucess",
                                "error": None,
                                "data": task
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
                            "status": "failed",
                            "error": None,
                            "data": {
                                "message": f"Internal Server Error!!"
                            }
                        }),
                    status=500,
                    mimetype="application/json"
                )

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

@task.route('/updatetask/<int:task_id>', methods = ['PATCH'])
@jwt_required    
def update_task(task_id = None):
    try:
        if id:
            pass

        data = request.json
        task_id = request.args.get('id')
        task_obj = task_repository.get_task_by_id(int(task_id))
        if not task_obj:
            return Response(json.dumps(
                            {
                                "status": "Sucess",
                                "error": None,
                                "data": {
                                    "message": f"No such Id exists!!"
                            }
                        }),
                        status=200,
                        mimetype="application/json"
                        )
        else:
            task_repository.update_task(data,task_obj)
            return Response(json.dumps(
                            {
                                "status": "Sucess",
                                "error": None,
                                "data": {
                                    "message": "Task Updated Successfully!!"
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
                            "status": "failed",
                            "error": None,
                            "data": {
                                "message": f"Internal Server Error!!"
                            }
                        }),
                    status=500,
                    mimetype="application/json"
                )
    
@task.route('/deletetask', methods = ['DELETE'])
@jwt_required
def delete_task():
    try:
        task_id = request.args.get('id')
        task_obj = task_repository.get_task_by_id(int(task_id))
        if not task_obj:
            return Response(json.dumps(
                            {
                                "status": "Sucess",
                                "error": None,
                                "data": {
                                    "message": f"No such Id exists!!"
                            }
                        }),
                        status=200,
                        mimetype="application/json"
                        )
        else:
            task_repository.delete_task(task_obj)
            return Response(json.dumps(
                            {
                                "status": "Sucess",
                                "error": None,
                                "data": {
                                    "message": "Task Deleted Successfully!!"
                            }
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