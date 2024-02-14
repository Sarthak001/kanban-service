from src import db
from src.models.task_model import Task

def get_task_by_id():
    pass

def get_all_tasks():
    pass

def update_task():
    pass

def delete_task():
    pass

def create_task(task_name,board_id,board_list_id):
    task_obj = Task(
            task_name = task_name,
            board_id_fk = board_id,
            board_list_fk = board_list_id
        )
    db.session.add(task_obj)
    db.session.commit()

