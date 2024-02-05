from flask import Blueprint
from src.controllers.auth_controller import auth
from src.controllers.board_controller import board


# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(auth, url_prefix="/auth")
api.register_blueprint(board,url_prefix = "/board")