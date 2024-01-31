from src import db


class Board(db.Model):
    __tablename__ ="board"
    board_id = db.Column(db.Integer(), primary_key=True,nullable = False)
    board_name = db.Column(db.String(20),nullable = False)
    board_owner_fk = db.Column(db.Integer(), db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    board_member = db.relationship("BoardMember",backref = "board")
    board_list = db.relationship("BoardList",backref= "board")