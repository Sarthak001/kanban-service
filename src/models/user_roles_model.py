from src import db
from . import user_model


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), unique=True, nullable=False)
    role_id = db.relationship("User", backref="user_roles",lazy="select", uselist=False)
    role = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
