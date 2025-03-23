from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL, IS_PRODUCTION

# Create the SQLAlchemy engine with appropriate settings
# For SQLite (development), we need check_same_thread=False
# For PostgreSQL (production), we don't use this parameter
if IS_PRODUCTION or not DATABASE_URL.startswith('sqlite'):
    # PostgreSQL or other production database
    engine = create_engine(DATABASE_URL)
else:
    # SQLite for development
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 