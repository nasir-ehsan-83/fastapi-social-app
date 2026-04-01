from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.db.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default = "True", nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), server_default = text("now()"), nullable = False)
    owner_id = Column(Integer, ForeignKey("user.id", ondelete = "CASCADE"), nullable = False)
    owner = relationship("User")

    def __repo__(self):
        return f"<Post id:{self.id} title: {self.title} owner_id: {self.owner_id}>"