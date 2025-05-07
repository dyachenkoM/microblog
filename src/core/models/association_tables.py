from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserKey(Base):
    __tablename__ = "users_keys"

    api_key: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True)


class FollowersTable(Base):
    __tablename__ = "followers"

    follower_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    following_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)


class TweetLikes(Base):
    __tablename__ = "tweets_likes"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    tweet_id: Mapped[int] = mapped_column(Integer, ForeignKey("tweets.id"), primary_key=True)


class TweetAttachment(Base):
    __tablename__ = "tweets_attachments"

    tweet_id: Mapped[int] = mapped_column(Integer, ForeignKey("tweets.id"), primary_key=True)
    attachment_id: Mapped[int] = mapped_column(Integer, ForeignKey("attachments.id"), primary_key=True)
