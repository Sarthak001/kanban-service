from src import db
from datetime import datetime


class UserRole(db.Model):
    __tablename__ = "user_roles"
    role_id = db.Column(db.Integer(), primary_key=True,nullable=False, autoincrement=False)
    role_name = db.Column(db.String(20))
    description = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
