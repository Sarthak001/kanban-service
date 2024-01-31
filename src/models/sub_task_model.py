from src import db
from datetime import datetime, timedelta


def customFunc():
    duedate = datetime.now() + timedelta(days=15)
    return duedate


class SubTask(db.Model):
    __tablename__ = "sub_tasks"
    id = db.Column(db.Integer(),primary_key = True,nullable = False)
    parent_task = db.Column(db.Integer(),db.ForeignKey('tasks.id'),nullable = False)
    sub_task_id = db.Column(db.Integer(),default = 1000, autoincrement = True)
    sub_task_description = db.Column(db.String(20),nullable = True)
    assigned_to = db.Column(db.Integer,db.ForeignKey('users.user_id'),nullable = True)
    is_check = db.Column(db.Boolean(),nullable = True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    due_date = db.Column(db.DateTime, default=customFunc(), nullable=False)
