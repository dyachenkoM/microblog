from .association_tables import TweetAttachment, TweetLikes
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from typing import List


class Tweet(Base):
    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    author: Mapped["User"] = relationship(back_populates="tweets")
    attachments: Mapped[List["Attachment"]] = relationship(
        secondary=TweetAttachment.__table__,
        back_populates="tweets",
        lazy="joined",
    )
    likes: Mapped[List["User"]] = relationship(
        secondary=TweetLikes.__table__,
        back_populates="liked_tweets",
        lazy="joined",
    )


from .user import User  # noqa
from .attachment import Attachment # noqa