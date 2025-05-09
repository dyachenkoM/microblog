from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from typing import List

from .association_tables import TweetAttachment
from .base import Base


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    link: Mapped[str] = mapped_column(String)

    tweets: Mapped[List["Tweet"]] = relationship(
        secondary=TweetAttachment.__table__,
        back_populates="attachments",
        lazy="joined",
        cascade="all, delete-orphan"
    )


from .tweet import Tweet  # noqa