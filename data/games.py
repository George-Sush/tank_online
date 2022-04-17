import sqlalchemy
from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_1 = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_2 = sqlalchemy.Column(sqlalchemy.String, nullable=False)
