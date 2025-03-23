from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class AlertRule(Base):
    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    description = Column(String(500))
    severity = Column(Integer)
    condition_type = Column(String(50))
    threshold = Column(Integer)
    check_interval = Column(Integer)
    notification_channels = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Relationship will be set after all models are defined

AlertRule.alert_records = relationship("AlertRecord", back_populates="alert_rule")