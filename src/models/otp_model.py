from src import db
from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func


class Otp(db.Model):
    __tablename__ = 'otp'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    user_id_fk = db.Column(db.Integer(), db.ForeignKey(
        'users.user_id'), nullable=False)
    otp = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(TIMESTAMP(timezone=True), nullable=False,
                           server_default=sqlalchemy.sql.expression.text('now()'))
    expire_in = db.Column(TIMESTAMP(timezone=True), nullable=False,
                          server_default=sqlalchemy.sql.expression.text('now()'))
