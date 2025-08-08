#!/usr/bin/env python3

import os
import sys
sys.path.append('.')

from app.database import engine, create_tables, User, SessionLocal

def test_database_connection():
    print("=== Testing Database Connection ===")
    
    try:
        # Test connection
        with engine.connect() as connection:
            print("✅ Database connection successful")
        
        # Create tables
        create_tables()
        print("✅ Tables created successfully")
        
        # Test user creation
        db = SessionLocal()
        try:
            # Check if test user exists
            user = db.query(User).filter(User.username == "test").first()
            if user:
                print(f"✅ Test user found: {user.username} (ID: {user.id})")
            else:
                print("❌ Test user not found")
                
            # Create test user if not exists
            if not user:
                new_user = User(
                    username="test",
                    email="test@shadow-goose.com",
                    role="admin"
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                print(f"✅ Test user created: {new_user.username} (ID: {new_user.id})")
                
        except Exception as e:
            print(f"❌ Error with user operations: {e}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

if __name__ == "__main__":
    test_database_connection() 