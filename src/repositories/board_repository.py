from src import db
from src.models.board_model import Board


def get_board_by_id(id):
    db_res = db.session.query(Board).filter(Board.board_id == id).first()
    return db_res

def get_board_owned(id):
    db_res = db.session.query(Board).filter(Board.board_owner_fk == id).all()
    return db_res

def get_all_boards():
    boards = Board.query.all()
    return boards

def update_board(d,board_obj):
    for key, value in d.items():
                if hasattr(Board,key):
                    setattr(board_obj,key,value)
    db.session.commit()

def delete_board(board_obj):
    db.session.delete(board_obj)
    db.session.commit()

def create_board(boardname,id):
    board_obj = Board(
                board_name  = boardname,
                board_owner_fk = id
                )
    db.session.add(board_obj)
    db.session.commit()

