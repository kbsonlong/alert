from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models.alert_record_model import AlertRecord
from pydantic import BaseModel

router = APIRouter(prefix="/api/alert-records", tags=["alert_records"])

class AlertRecordBase(BaseModel):
    alert_rule_id: int
    status: str
    severity: int
    description: str
    source: str
    target: str
    resolution_note: str | None = None
    handled_by: str | None = None

class AlertRecordCreate(AlertRecordBase):
    pass

class AlertRecordUpdate(BaseModel):
    status: str
    resolution_note: str = None
    handled_by: str = None

class AlertRecordResponse(AlertRecordBase):
    id: int
    first_occurrence_time: datetime
    last_occurrence_time: datetime
    resolution_time: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

@router.post("/", response_model=AlertRecordResponse)
def create_alert_record(alert_record: AlertRecordCreate, db: Session = Depends(get_db)):
    alert_data = alert_record.dict()
    if alert_data.get('status') == 'resolved' or alert_data.get('status') == 'closed':
        alert_data['resolution_time'] = datetime.now()
    db_alert_record = AlertRecord(**alert_data)
    db.add(db_alert_record)
    db.commit()
    db.refresh(db_alert_record)
    return db_alert_record

@router.get("/", response_model=List[AlertRecordResponse])
def get_alert_records(skip: int = 0, limit: int = 100, status: str = None, db: Session = Depends(get_db)):
    query = db.query(AlertRecord)
    if status:
        query = query.filter(AlertRecord.status == status)
    return query.offset(skip).limit(limit).all()

@router.get("/{record_id}", response_model=AlertRecordResponse)
def get_alert_record(record_id: int, db: Session = Depends(get_db)):
    db_alert_record = db.query(AlertRecord).filter(AlertRecord.id == record_id).first()
    if db_alert_record is None:
        raise HTTPException(status_code=404, detail="Alert record not found")
    return db_alert_record

@router.put("/{record_id}", response_model=AlertRecordResponse)
def update_alert_record(record_id: int, alert_record: AlertRecordUpdate, db: Session = Depends(get_db)):
    db_alert_record = db.query(AlertRecord).filter(AlertRecord.id == record_id).first()
    if db_alert_record is None:
        raise HTTPException(status_code=404, detail="Alert record not found")
    
    update_data = alert_record.dict(exclude_unset=True)
    if 'status' in update_data and update_data['status'] == 'resolved':
        update_data['resolution_time'] = datetime.now()
    
    for key, value in update_data.items():
        setattr(db_alert_record, key, value)
    
    db.commit()
    db.refresh(db_alert_record)
    return db_alert_record

@router.delete("/{record_id}")
def delete_alert_record(record_id: int, db: Session = Depends(get_db)):
    db_alert_record = db.query(AlertRecord).filter(AlertRecord.id == record_id).first()
    if db_alert_record is None:
        raise HTTPException(status_code=404, detail="Alert record not found")
    
    db.delete(db_alert_record)
    db.commit()
    return {"message": "Alert record deleted successfully"}