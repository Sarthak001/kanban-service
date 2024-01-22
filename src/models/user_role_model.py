from src import db
from datetime import datetime
import sqlalchemy
from sqlalchemy.sql.sqltypes import TIMESTAMP


class UserRole(db.Model):
    __tablename__ = "user_roles"
    role_id = db.Column(db.Integer(), primary_key=True,
                        nullable=False, autoincrement=False)
    role_name = db.Column(db.String(20))
    description = db.Column(db.String(50))
    created_at = db.Column(TIMESTAMP(timezone=True), nullable=False,
                           server_default=sqlalchemy.sql.expression.text('now()'))
    updated_at = db.Column(TIMESTAMP(timezone=True), nullable=False,
                           server_default=sqlalchemy.sql.expression.text('now() ON UPDATE CURRENT_TIMESTAMP'))
