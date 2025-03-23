from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class AlertRecord(Base):
    __tablename__ = "alert_records"

    id = Column(Integer, primary_key=True, index=True)
    alert_rule_id = Column(Integer, ForeignKey('alert_rules.id'))
    status = Column(String(20))  # pending, processing, resolved, closed
    severity = Column(Integer)
    description = Column(String(1000))
    source = Column(String(200))
    target = Column(String(200))
    first_occurrence_time = Column(DateTime, default=datetime.now)
    last_occurrence_time = Column(DateTime, default=datetime.now)
    resolution_time = Column(DateTime, nullable=True)
    resolution_note = Column(String(1000), nullable=True)
    handled_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Relationship will be set after all models are defined

AlertRecord.alert_rule = relationship("AlertRule", back_populates="alert_records")
AlertRecord.notification_records = relationship("NotificationRecord", back_populates="alert_record")