from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models.analysis_record_model import AnalysisRecord
from models.alert_record_model import AlertRecord
from pydantic import BaseModel
import requests

router = APIRouter(prefix="/api/analysis-records", tags=["analysis_records"])

class AnalysisRecordBase(BaseModel):
    alert_id: int
    status: str
    analysis_result: str = None
    error_message: str = None

class AnalysisRecordCreate(AnalysisRecordBase):
    pass

class AnalysisRecordResponse(AnalysisRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None
    error_message: str | None = None

    class Config:
        orm_mode = True

async def analyze_alert(alert_id: int, db: Session):
    try:
        alert_record = db.query(AlertRecord).filter(AlertRecord.id == alert_id).first()
        alert_msg = f"告警描述：{alert_record.description}"
        print(alert_msg)
        # 调用Ollama服务进行分析
        response = requests.post(
            "http://10.98.65.131:11434/api/generate",
            json={
                "model": "deepseek-r1:32b",
                "prompt": f"分析告警 {alert_msg} 的可能原因和解决方案,请从以下几个方面进行分析：\n1. 告警的严重程度和影响范围\n2. 可能的原因分析\n3. 建议的处理方案\n4. 预防措施建议\n请用中文回答，并保持专业和客观。"
            }
        )
        result = response.json()
        
        # 更新分析记录
        db_record = db.query(AnalysisRecord).filter(AnalysisRecord.alert_id == alert_id).first()
        if db_record:
            db_record.status = "completed"
            db_record.analysis_result = result.get('response', '')
            db_record.completed_at = datetime.now()
            db.commit()
            db.refresh(db_record)
    except Exception as e:
        # 更新错误信息
        print(f"Error during analysis: {str(e)}")
        db_record = db.query(AnalysisRecord).filter(AnalysisRecord.alert_id == alert_id).first()
        if db_record:
            db_record.status = "completed"
            db_record.error_message = str(e)
            db_record.completed_at = datetime.now()
            db.commit()

@router.post("/analyze/{alert_id}", response_model=AnalysisRecordResponse)
def create_analysis(alert_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 检查是否已存在分析记录
    existing_record = db.query(AnalysisRecord).filter(AnalysisRecord.alert_id == alert_id).first()
    if existing_record:
        return existing_record
    
    # 创建新的分析记录
    db_record = AnalysisRecord(
        alert_id=alert_id,
        status="processing",
        analysis_result=""
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    # 启动异步分析任务
    background_tasks.add_task(analyze_alert, alert_id, db)
    
    return db_record

@router.get("/{alert_id}", response_model=AnalysisRecordResponse)
def get_analysis_record(alert_id: int, db: Session = Depends(get_db)):
    db_record = db.query(AnalysisRecord).filter(AnalysisRecord.alert_id == alert_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail="Analysis record not found")
    return db_record