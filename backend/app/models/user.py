from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String(50), nullable = False)
    username = Column(String(30), nullable = False, unique = True)
    email = Column(String(255), nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), server_default = text("now()"), nullable = False)

    def __repr__(self):
        return f"<User id={self.id} username={self.username} email={self.email}>"