from src import db,bcrypt
from src.models.user_model import User
from src.models.user_role_model import UserRole
from random import randint



def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user

def get_user_role():
    role = db.session.query(UserRole.role_id).filter(UserRole.role_name == "normal user").first()
    return role

def get_all_users():
    user_obj = User.query.all() # will fetch all the records. Iterate over user_obj to access each row in db.

def update_user():
    pass

def delete_user():
    pass

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
