from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign
from sqlalchemy import String, Integer
from typing import List

from .association_tables import FollowersTable
from .base import Base


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

    tweets: Mapped[List["Tweet"]] = relationship(
        back_populates="author",
        lazy="dynamic",
    )

    liked_tweets: Mapped[List["Tweet"]] = relationship(
        secondary="tweets_likes",
        back_populates="likes",
        lazy="dynamic",
    )


from .tweet import Tweet  # noqa