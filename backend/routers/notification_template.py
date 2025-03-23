from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models.notification_template_model import NotificationTemplate
from pydantic import BaseModel

router = APIRouter(prefix="/api/notification-templates", tags=["notification_templates"])

class NotificationTemplateBase(BaseModel):
    name: str
    description: str
    template_type: str
    content: str
    variables: dict
    language: str = 'zh-CN'
    is_active: bool = True

class NotificationTemplateCreate(NotificationTemplateBase):
    pass

class NotificationTemplateUpdate(NotificationTemplateBase):
    pass

class NotificationTemplateResponse(NotificationTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@router.post("/", response_model=NotificationTemplateResponse)
def create_notification_template(template: NotificationTemplateCreate, db: Session = Depends(get_db)):
    db_template = NotificationTemplate(**template.dict())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

@router.get("/", response_model=List[NotificationTemplateResponse])
def get_notification_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(NotificationTemplate).offset(skip).limit(limit).all()

@router.get("/{template_id}", response_model=NotificationTemplateResponse)
def get_notification_template(template_id: int, db: Session = Depends(get_db)):
    db_template = db.query(NotificationTemplate).filter(NotificationTemplate.id == template_id).first()
    if db_template is None:
        raise HTTPException(status_code=404, detail="Notification template not found")
    return db_template

@router.put("/{template_id}", response_model=NotificationTemplateResponse)
def update_notification_template(template_id: int, template: NotificationTemplateUpdate, db: Session = Depends(get_db)):
    db_template = db.query(NotificationTemplate).filter(NotificationTemplate.id == template_id).first()
    if db_template is None:
        raise HTTPException(status_code=404, detail="Notification template not found")
    
    for key, value in template.dict().items():
        setattr(db_template, key, value)
    
    db.commit()
    db.refresh(db_template)
    return db_template

@router.delete("/{template_id}")
def delete_notification_template(template_id: int, db: Session = Depends(get_db)):
    db_template = db.query(NotificationTemplate).filter(NotificationTemplate.id == template_id).first()
    if db_template is None:
        raise HTTPException(status_code=404, detail="Notification template not found")
    
    db.delete(db_template)
    db.commit()
    return {"message": "Notification template deleted successfully"}