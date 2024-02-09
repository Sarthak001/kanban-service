from flask import Blueprint
from src.controllers.auth_controller import auth
from src.controllers.board_controller import board
from src.controllers.task_controller import task


# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(auth, url_prefix="/auth")
api.register_blueprint(board,url_prefix = "/board")
api.register_blueprint(task,url_prefix = "/task")