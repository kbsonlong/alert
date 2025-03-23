from sqlalchemy import Column, Integer, String, Text, ARRAY, DateTime
from sqlalchemy.sql import func
from database import Base

class KnowledgeBase(Base):
    __tablename__ = "knowledge_bases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    source_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(ARRAY(String))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer)