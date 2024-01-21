from flask import request, Response, json, Blueprint
from src.models.user_model import User
from src import bcrypt, db
from datetime import datetime
import jwt
import os

# user controller blueprint to be registered with api blueprint
users = Blueprint("users", __name__)

# route for signup api/users/signup
@users.route('/signup', methods = ["POST"])
def handle_signup():
    return
# route for login api/users/signin
@users.route('/signin', methods = ["POST"])
def handle_login():
    return