from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class NotificationGroup(Base):
    __tablename__ = "notification_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    description = Column(String(500))
    members = Column(JSON)  # List of member contacts
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class NotificationChannel(Base):
    __tablename__ = "notification_channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    channel_type = Column(String(50))  # email, sms, webhook
    config = Column(JSON)  # Channel specific configuration
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class NotificationRecord(Base):
    __tablename__ = "notification_records"

    id = Column(Integer, primary_key=True, index=True)
    alert_record_id = Column(Integer, ForeignKey('alert_records.id'))
    notification_group_id = Column(Integer, ForeignKey('notification_groups.id'))
    notification_channel_id = Column(Integer, ForeignKey('notification_channels.id'))
    status = Column(String(20))  # pending, sent, failed
    content = Column(String(2000))
    error_message = Column(String(500), nullable=True)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    alert_record = relationship("AlertRecord", back_populates="notification_records")
    notification_group = relationship("NotificationGroup")
    notification_channel = relationship("NotificationChannel")