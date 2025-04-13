from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign
from sqlalchemy import String, Integer, ForeignKey
from typing import List
from .base import Base


class FollowersTable(Base):
    __tablename__ = "followers"

    follower_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    following_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    followers: Mapped[List["User"]] = relationship(
        secondary=FollowersTable.__table__,
        primaryjoin=id == foreign(FollowersTable.following_id),
        secondaryjoin=id == foreign(FollowersTable.follower_id),
        back_populates="following",
        lazy="joined",
    )

    following: Mapped[List["User"]] = relationship(
        secondary=FollowersTable.__table__,
        primaryjoin=id == foreign(FollowersTable.follower_id),
        secondaryjoin=id == foreign(FollowersTable.following_id),
        back_populates="followers",
        lazy="joined",
    )

