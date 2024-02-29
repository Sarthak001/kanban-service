from src import db
from src.models.task_model import Task


def get_task_by_board_id(id):
    db_res = db.session.query(Task).filter(Task.board_id_fk==id).all()
    return db_res

def get_task_assigned_to_me(id):
    db_res = db.session.query(Task).filter(Task.assigned_to == id).all()
    return db_res

def get_task_by_id(id):
    db_res = db.session.query(Task).filter(Task.task_id ==id).all()
    return db_res

def get_all_tasks():
    task = Task.query.all()
    return task

def update_task(d,task_obj):
    for key, value in d.items():
                if hasattr(Task,key):
                    setattr(task_obj[0],key,value)
    db.session.commit()

def delete_task(task_obj):
    db.session.delete(task_obj)
    db.session.commit()

def create_task(data,task_description = None,priority = None,assigned_to = None):
    if "task_description" in data : task_description = data['task_description']
    if "priority" in data : priority = data['priority']
    if "assigned_to" in data : assigned_to = int(data['assigned_to'])

    task_obj = Task(
            task_name = data['task_name'],
            board_id_fk = int(data['board_id_fk']),
            board_list_fk = int(data['board_list_fk']),
            task_description = task_description,
            priority = priority,
            assigned_to = assigned_to,
        )
    db.session.add(task_obj)
    db.session.commit()

