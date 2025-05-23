from sqlalchemy.ext.hybrid import hybrid_property

from .association_tables import TweetAttachment, TweetLikes
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, select, func
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
        cascade="all, delete",
        single_parent=True,
    )
    likes: Mapped[List["User"]] = relationship(
        secondary=TweetLikes.__table__,
        back_populates="liked_tweets",
        lazy="joined",
    )

    @hybrid_property
    def likes_count(self):
        if hasattr(self, "_likes_count"):
            return self._likes_count
        return len(self.likes) if hasattr(self, "likes") else 0

    @likes_count.expression
    def likes_count(cls):
        return (
            select(func.count(TweetLikes.user_id))
            .where(TweetLikes.tweet_id == cls.id)
            .label("likes_count")
        )


from .user import User  # noqa
from .attachment import Attachment  # noqa
