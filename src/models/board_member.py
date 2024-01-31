from src import db


class BoardMember(db.Model):
    __tablename__ ="board_members"
    id = db.Column(db.Integer(),primary_key = True, nullable = False)
    member_fk = db.Column(db.Integer(), db.ForeignKey('users.user_id'),nullable = False)
    board_id_fk = db.Column(db.Integer(), db.ForeignKey('board.board_id'),nullable = False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now(), nullable=True)