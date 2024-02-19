from src import db,bcrypt
from src.models.user_model import User
from src.models.user_role_model import UserRole
from random import randint

def get_user_by_id(id):
    user = User.query.filter_by(user_id = id).first()
    return user

def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user

def get_user_role(user_role = None):
    if user_role == None :
        user_role = "normalusers"
    role = db.session.query(UserRole.role_id).filter(UserRole.role_name == user_role).first()
    return role

def get_all_users():
    user_obj = User.query.all()
    return user_obj # will fetch all the records. Iterate over user_obj to access each row in db.

def create_user(role,firstname,lastname,email,password):
    user_obj = User(
                    role_id_fk=role[0],
                    user_name= firstname + lastname + str(randint(10, 99)),
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    passwd=bcrypt.generate_password_hash(password).decode('utf-8'),
                    is_active=False,
                )
    db.session.add(user_obj)
    db.session.commit()
    return user_obj

def update_user_password(user,password):
    user.passwd = bcrypt.generate_password_hash(password).decode('utf-8')
    db.session.add(user)
    db.session.commit()

def update_user_active(user):
    user.is_active = True
    db.session.commit()


def delete_user():
    pass
