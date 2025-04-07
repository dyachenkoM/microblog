from sqlalchemy import Column, Integer, String
from core.models.db_helper import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    followers = Column(Integer, default=0)
    following = Column(Integer)
