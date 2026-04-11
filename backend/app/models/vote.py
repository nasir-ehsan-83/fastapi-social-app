from sqlalchemy import Column, Integer, ForeignKey, Enum as EnumSQL
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.user import User
from app.models.post import Post
from app.enums.vote_enum import ReactionType


class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    type = Column(EnumSQL(ReactionType), nullable = False)

    user = relationship("User", back_populates="votes")
    post = relationship("Post", back_populates="votes")