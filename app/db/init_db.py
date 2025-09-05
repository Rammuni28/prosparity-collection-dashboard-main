from app.core.config import settings
from sqlalchemy import create_engine
from app.models import Base
from app.db.session import SessionLocal

# Create database engine
engine = create_engine(settings.DATABASE_URL)

# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    init_db()
