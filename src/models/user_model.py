from src import db


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer(), primary_key=True)
    role_id_fk = db.Column(db.Integer(), db.ForeignKey('user_roles.role_id'), nullable=False)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(80), unique=True, nullable=False)
    passwd = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    last_login = db.Column(db.DateTime,nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now(), nullable=True)

    role = db.relationship("UserRole")
    otp = db.relationship("Otp", backref='users')
