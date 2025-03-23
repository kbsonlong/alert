from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models.alert_rule_model import AlertRule
from pydantic import BaseModel

router = APIRouter(prefix="/api/alert-rules", tags=["alert_rules"])

class AlertRuleBase(BaseModel):
    name: str
    description: str
    severity: int
    condition_type: str
    threshold: int
    check_interval: int
    notification_channels: str
    is_active: bool = True

class AlertRuleCreate(AlertRuleBase):
    pass

class AlertRuleUpdate(AlertRuleBase):
    pass

class AlertRuleResponse(AlertRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@router.post("/", response_model=AlertRuleResponse)
def create_alert_rule(alert_rule: AlertRuleCreate, db: Session = Depends(get_db)):
    db_alert_rule = AlertRule(**alert_rule.dict())
    db.add(db_alert_rule)
    db.commit()
    db.refresh(db_alert_rule)
    return db_alert_rule

@router.get("/", response_model=List[AlertRuleResponse])
def get_alert_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(AlertRule).offset(skip).limit(limit).all()

@router.get("/{rule_id}", response_model=AlertRuleResponse)
def get_alert_rule(rule_id: int, db: Session = Depends(get_db)):
    db_alert_rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if db_alert_rule is None:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    return db_alert_rule

@router.put("/{rule_id}", response_model=AlertRuleResponse)
def update_alert_rule(rule_id: int, alert_rule: AlertRuleUpdate, db: Session = Depends(get_db)):
    db_alert_rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if db_alert_rule is None:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    
    for key, value in alert_rule.dict().items():
        setattr(db_alert_rule, key, value)
    
    db.commit()
    db.refresh(db_alert_rule)
    return db_alert_rule

@router.delete("/{rule_id}")
def delete_alert_rule(rule_id: int, db: Session = Depends(get_db)):
    db_alert_rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
    if db_alert_rule is None:
        raise HTTPException(status_code=404, detail="Alert rule not found")
    
    db.delete(db_alert_rule)
    db.commit()
    return {"message": "Alert rule deleted successfully"}