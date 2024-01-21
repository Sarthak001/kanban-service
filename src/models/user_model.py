from src import db
from . import user_roles_model


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    first_name = db.Column(db.String(60))
    lastname = db.Column(db.String(60))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.Integer(), db.ForeignKey('user_roles.role_id'), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
