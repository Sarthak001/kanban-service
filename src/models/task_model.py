from src import db
from datetime import datetime, timedelta
from sqlalchemy.schema import Sequence


def customFunc():
    duedate = datetime.now() + timedelta(days=15)
    return duedate


class Task(db.Model):
    __tablename__ = "tasks"
    task_id = db.Column(db.Integer(),Sequence('task_id_seq', start=1000, increment=1),primary_key = True,nullable = False)
    task_name = db.Column(db.String(20),nullable = False)
    task_description = db.Column(db.String(20),nullable = True)
    priority = db.Column(db.String(20),nullable = True)
    assigned_to = db.Column(db.Integer,db.ForeignKey('users.user_id'),nullable = True)
    state = db.Column(db.String(10),nullable = True)
    board_id_fk = db.Column(db.Integer(),db.ForeignKey('board.board_id'),nullable = False)
    board_list_fk = db.Column(db.Integer(),db.ForeignKey('board_list.board_list_id'),nullable = False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    due_date = db.Column(db.DateTime, default=customFunc(), nullable=False)


    sub_task = db.relationship("SubTask",backref="tasks")
