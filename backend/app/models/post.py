from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.db.database import Base
from app.models.user import User
from app.enums.post import PostStatus, PostType, PostVisibility

class Post(Base):
    __tablename__ = "posts"

    id = Column(
        Integer, 
        primary_key = True, 
        nullable = False
    )

    title = Column(
        String, 
        nullable = False
    )

    content = Column(
        String, 
        nullable = False
    )

    post_status = Column(
        SQLEnum(PostStatus),
        nullable = False,
        server_default = "published"
    )

    post_type = Column(
        SQLEnum(PostType),
        nullable = False
    )

    post_visibility = Column(
        SQLEnum(PostVisibility),
        nullable = False
    )

    post_media_url = Column(
        String, 
        nullable = False
    )

    owner_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete = "CASCADE"), 
        nullable = False
    )

    created_at = Column(
        TIMESTAMP(timezone = True), 
        server_default = text("now()"), 
        nullable = False
    )

    updated_at = Column(
        TIMESTAMP(timezone = True),
        server_default = text("now()"),
        nullable = False
    )

    owner = relationship("User", lazy = "joined")

    def __repo__(self):
        return f"<Post id:{self.id} title: {self.title} owner_id: {self.owner_id}>"