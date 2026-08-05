from sqlalchemy import Column, Integer, String, Boolean
from server.app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    username = Column(String, nullable=True)
    firstname = Column(String, nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False, server_default="false")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username}, firstname={self.firstname})>"
