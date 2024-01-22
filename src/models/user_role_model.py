from src import db


class UserRole(db.Model):
    __tablename__ = "user_roles"
    role_id = db.Column(db.Integer(), primary_key=True, nullable=False,autoincrement=False)
    role_name = db.Column(db.String(20))
    description = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)