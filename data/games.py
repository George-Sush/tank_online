import sqlalchemy
from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    users = sqlalchemy.Column(sqlalchemy.String)
