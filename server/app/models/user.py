from sqlalchemy import Column, Integer, String
from server.app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.telegram_id}, email={self.email})>"