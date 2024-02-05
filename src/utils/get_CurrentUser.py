from flask import request
import jwt
import os


def get_CurrentUser():
    headers = request.headers
    bearer = headers.get('Authorization')   # Bearer YourTokenHere
    token = bearer.split()[1]
    decoded_data = jwt.decode(jwt=token, key = os.getenv('SECRET_KEY'), algorithms=['HS256'])
    return decoded_data