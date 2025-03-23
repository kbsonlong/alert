from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from database import Base
from datetime import datetime

class NotificationTemplate(Base):
    __tablename__ = "notification_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    description = Column(String(500))
    template_type = Column(String(50))  # email, sms, webhook
    content = Column(String(2000))
    variables = Column(JSON)  # Dictionary of available variables with their descriptions
    language = Column(String(10), default='zh-CN')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)