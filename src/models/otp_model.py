from src import db
from datetime import datetime, timedelta


class Otp(db.Model):
    __tablename__ = 'otp'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.user_id'), nullable=False)
    otp = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    expire_in = db.Column(db.DateTime, nullable=False,
                          default=datetime.now() + timedelta(minutes=10))
