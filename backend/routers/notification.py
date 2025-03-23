from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models.notification_model import NotificationGroup, NotificationChannel
from pydantic import BaseModel

router = APIRouter(prefix="/api/notifications", tags=["notifications"])

class NotificationGroupBase(BaseModel):
    name: str
    description: str
    members: List[dict]
    is_active: bool = True

class NotificationGroupCreate(NotificationGroupBase):
    pass

class NotificationGroupUpdate(NotificationGroupBase):
    pass

class NotificationGroupResponse(NotificationGroupBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class NotificationChannelBase(BaseModel):
    name: str
    channel_type: str
    config: dict
    is_active: bool = True

class NotificationChannelCreate(NotificationChannelBase):
    pass

class NotificationChannelUpdate(NotificationChannelBase):
    pass

class NotificationChannelResponse(NotificationChannelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Notification Group APIs
@router.post("/groups/", response_model=NotificationGroupResponse)
def create_notification_group(group: NotificationGroupCreate, db: Session = Depends(get_db)):
    db_group = NotificationGroup(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.get("/groups/", response_model=List[NotificationGroupResponse])
def get_notification_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(NotificationGroup).offset(skip).limit(limit).all()

@router.get("/groups/{group_id}", response_model=NotificationGroupResponse)
def get_notification_group(group_id: int, db: Session = Depends(get_db)):
    db_group = db.query(NotificationGroup).filter(NotificationGroup.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Notification group not found")
    return db_group

@router.put("/groups/{group_id}", response_model=NotificationGroupResponse)
def update_notification_group(group_id: int, group: NotificationGroupUpdate, db: Session = Depends(get_db)):
    db_group = db.query(NotificationGroup).filter(NotificationGroup.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Notification group not found")
    
    for key, value in group.dict().items():
        setattr(db_group, key, value)
    
    db.commit()
    db.refresh(db_group)
    return db_group

@router.delete("/groups/{group_id}")
def delete_notification_group(group_id: int, db: Session = Depends(get_db)):
    db_group = db.query(NotificationGroup).filter(NotificationGroup.id == group_id).first()
    if db_group is None:
        raise HTTPException(status_code=404, detail="Notification group not found")
    
    db.delete(db_group)
    db.commit()
    return {"message": "Notification group deleted successfully"}

# Notification Channel APIs
@router.post("/channels/", response_model=NotificationChannelResponse)
def create_notification_channel(channel: NotificationChannelCreate, db: Session = Depends(get_db)):
    db_channel = NotificationChannel(**channel.dict())
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

@router.get("/channels/", response_model=List[NotificationChannelResponse])
def get_notification_channels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(NotificationChannel).offset(skip).limit(limit).all()

@router.get("/channels/{channel_id}", response_model=NotificationChannelResponse)
def get_notification_channel(channel_id: int, db: Session = Depends(get_db)):
    db_channel = db.query(NotificationChannel).filter(NotificationChannel.id == channel_id).first()
    if db_channel is None:
        raise HTTPException(status_code=404, detail="Notification channel not found")
    return db_channel

@router.put("/channels/{channel_id}", response_model=NotificationChannelResponse)
def update_notification_channel(channel_id: int, channel: NotificationChannelUpdate, db: Session = Depends(get_db)):
    db_channel = db.query(NotificationChannel).filter(NotificationChannel.id == channel_id).first()
    if db_channel is None:
        raise HTTPException(status_code=404, detail="Notification channel not found")
    
    for key, value in channel.dict().items():
        setattr(db_channel, key, value)
    
    db.commit()
    db.refresh(db_channel)
    return db_channel

@router.delete("/channels/{channel_id}")
def delete_notification_channel(channel_id: int, db: Session = Depends(get_db)):
    db_channel = db.query(NotificationChannel).filter(NotificationChannel.id == channel_id).first()
    if db_channel is None:
        raise HTTPException(status_code=404, detail="Notification channel not found")
    
    db.delete(db_channel)
    db.commit()
    return {"message": "Notification channel deleted successfully"}