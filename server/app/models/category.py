from sqlalchemy import Column, Integer, String, Boolean
from server.app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    slug = Column(String, unique=True, index=True)
    action = Column(Boolean)

    def __repr__(self):
        return f"<Category id: {self.id}, name: {self.name}, slug: {self.slug}>"
