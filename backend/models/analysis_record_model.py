from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class AnalysisRecord(Base):
    __tablename__ = "analysis_records"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey('alert_records.id'))
    status = Column(String(20))  # pending, processing, completed
    analysis_result = Column(String(2000))
    error_message = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    completed_at = Column(DateTime, nullable=True)

    # Relationship
    alert_record = relationship("AlertRecord", backref="analysis_records")