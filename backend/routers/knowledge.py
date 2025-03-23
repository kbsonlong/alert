from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import httpx

from database import get_db
from models.knowledge_model import KnowledgeBase

router = APIRouter(
    prefix="/api/knowledge",
    tags=["knowledge"]
)

# Ollama API配置
OLLAMA_API_URL = "http://localhost:11434/api"

@router.get("", response_model=List[dict])
def get_knowledge_bases(db: Session = Depends(get_db)):
    return db.query(KnowledgeBase).all()

@router.post("")
def create_knowledge_base(knowledge: dict, db: Session = Depends(get_db)):
    db_knowledge = KnowledgeBase(**knowledge)
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge

@router.get("/{knowledge_id}")
def get_knowledge_base(knowledge_id: int, db: Session = Depends(get_db)):
    knowledge = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    return knowledge

@router.put("/{knowledge_id}")
def update_knowledge_base(knowledge_id: int, knowledge: dict, db: Session = Depends(get_db)):
    db_knowledge = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_id).first()
    if not db_knowledge:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    
    for key, value in knowledge.items():
        setattr(db_knowledge, key, value)
    
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge

@router.delete("/{knowledge_id}")
def delete_knowledge_base(knowledge_id: int, db: Session = Depends(get_db)):
    knowledge = db.query(KnowledgeBase).filter(KnowledgeBase.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    
    db.delete(knowledge)
    db.commit()
    return {"message": "Knowledge base deleted"}

@router.post("/query")
async def query_knowledge(query: dict):
    try:
        async with httpx.AsyncClient() as client:
            # 调用Ollama API进行知识库查询
            response = await client.post(
                f"{OLLAMA_API_URL}/generate",
                json={
                    "model": "llama2",
                    "prompt": query["query"],
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "content": result["response"],
                "metadata": {
                    "model": "llama2",
                    "total_duration": result.get("total_duration", 0)
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))