import sqlalchemy
from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = "games"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_1 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user_2 = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    field_1 = sqlalchemy.Column(sqlalchemy.String)
    field_2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    flag = sqlalchemy.Column(
        sqlalchemy.Boolean, default=True
    )  # тут кто ходит, a на следующей номер игрока, который
    flag_win = sqlalchemy.Column(
        sqlalchemy.Integer, default=0
    )  # победил (если 0, то ещё такового нет)
