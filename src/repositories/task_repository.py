from src import db
from src.models.task_model import Task

def get_task_by_board_id(id):
    db_res = db.session.query(Task).filter(Task.board_id_fk==id).all()
    return db_res

def get_task_assigned_to_me(id):
    db_res = db.session.query(Task).filter(Task.assigned_to == id).all()
    return db_res

def get_task_by_id(id):
    db_res = db.session.query(Task).filter(Task.id ==id).all()
    return db_res

def get_all_tasks():
    pass

def update_task(d,task_obj):
    for key, value in d.items():
                if hasattr(Task,key):
                    setattr(task_obj[0],key,value)
    db.session.commit()

def delete_task(task_obj):
    db.session.delete(task_obj)
    db.session.commit()

def create_task(task_name,board_id,board_list_id):
    task_obj = Task(
            task_name = task_name,
            board_id_fk = board_id,
            board_list_fk = board_list_id
        )
    db.session.add(task_obj)
    db.session.commit()

