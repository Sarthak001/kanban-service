from src import db
from datetime import datetime, timedelta


def customFunc():
    expire = datetime.now() + timedelta(minutes=10)
    return expire


class PasswordReset(db.Model):
    __tablename__ = 'password_reset'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    user_id_fk = db.Column(db.Integer(), db.ForeignKey('users.user_id'), nullable=False)
    token = db.Column(db.String(100), nullable=False)
    consumed = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    expire_in = db.Column(db.DateTime, default=customFunc(), nullable=False)
