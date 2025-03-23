from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import alert_rule, alert_record, notification, notification_template, knowledge, analysis_record

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="AlertAgent API",
    description="运维告警管理系统API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(alert_rule.router)
app.include_router(alert_record.router)
app.include_router(analysis_record.router)
app.include_router(notification.router)
app.include_router(notification_template.router)
app.include_router(knowledge.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AlertAgent API"}