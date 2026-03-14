from sqlalchemy import Column, Integer, String, BigInteger
from server.app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    firstname = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.telegram_id}, email={self.username}, firstname={self.firstname})>"