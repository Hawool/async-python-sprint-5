from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from src.db.db import Base


class FileModel(Base):
    __tablename__ = "file_model"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    path = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), index=True, server_default=func.now())

    user_id = Column(UUID, ForeignKey("user.id"))
