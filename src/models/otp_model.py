from src import db
from datetime import datetime,timedelta

def customFunc():
    expire = datetime.now() + timedelta(minutes=10)
    return expire

class Otp(db.Model):
    __tablename__ = 'otp'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    user_id_fk = db.Column(db.Integer(), db.ForeignKey('users.user_id'), nullable=False)
    otp = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    expire_in = db.Column(db.DateTime, default=customFunc(),nullable=True)
