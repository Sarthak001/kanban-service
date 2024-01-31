from src import db

class BoardList(db.Model):
    __tablename__ = "board_list"
    board_list_id = db.Column(db.Integer(),primary_key = True,nullable= False)
    board_id_fk = db.Column(db.Integer(), db.ForeignKey('board.board_id'),nullable = False)
    list_name = db.Column(db.String(20),nullable = False)
    order = db.Column(db.Integer(),nullable = False)
