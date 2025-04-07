from sqlalchemy import Column, Integer, String
from .base import Base


class User(Base):
    __tablename__ = "users"

    name = Column(String, index=True)
    followers = Column(Integer, default=0)
    following = Column(Integer)
