from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base


class Item(Base):
    __tablename__ = "items"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at  = Column(DateTime, server_default=func.now())