from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://alert_user:alert_password@localhost/alert_agent')

# Create SQLAlchemy engine with retry mechanism
def create_engine_with_retry(url, max_retries=3, retry_interval=5):
    for attempt in range(max_retries):
        try:
            engine = create_engine(url, pool_pre_ping=True)
            # Test the connection
            engine.connect()
            return engine
        except OperationalError as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Database connection attempt {attempt + 1} failed. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)

# Create engine with retry mechanism
engine = create_engine_with_retry(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session with retry mechanism
def get_db():
    max_retries = 3
    retry_interval = 5
    
    for attempt in range(max_retries):
        try:
            db = SessionLocal()
            db.execute('SELECT 1')
            try:
                yield db
            finally:
                db.close()
            return
        except OperationalError as e:
            if attempt == max_retries - 1:
                raise e
            print(f"Database connection attempt {attempt + 1} failed. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
            if db:
                db.close()