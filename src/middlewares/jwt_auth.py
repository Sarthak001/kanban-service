from flask import Flask, request, jsonify
import jwt
from functools import wraps
import os


def jwt_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        # Get the JWT token from the request headers
        token = request.headers.get('Authorization').split()[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # Verify and decode the JWT token
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            # You can now access the payload data in your routes via request.current_user
            request.current_user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return route_function(*args, **kwargs)

    return wrapper