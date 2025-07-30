#!/usr/bin/env python3
"""Initialize database with admin user and sample data."""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.store import Store
from app.core.security import get_password_hash

def create_admin_user():
    """Create admin user and sample store."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("Admin user already exists")
        else:
            # Create admin user
            admin_user = User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                is_admin=True
            )
            db.add(admin_user)
            print("Created admin user: admin / admin123")
        
        # Check if sample store exists
        existing_store = db.query(Store).filter(Store.name == "코스트코 양평점").first()
        if existing_store:
            print("Sample store already exists")
        else:
            # Create sample store
            sample_store = Store(
                name="코스트코 양평점",
                address="서울특별시 영등포구 양평로",
            )
            db.add(sample_store)
            print("Created sample store: 코스트코 양평점")
        
        db.commit()
        print("Database initialization completed!")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user() 