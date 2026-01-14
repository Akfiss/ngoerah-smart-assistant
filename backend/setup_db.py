"""
Database Setup Script for Ngoerah Smart Assistant
Run this script to create database tables after PostgreSQL is configured.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_database():
    """Create all database tables"""
    print("=" * 50)
    print("Ngoerah Smart Assistant - Database Setup")
    print("=" * 50)
    
    try:
        from app.database import create_tables, engine
        from app.models.database import Base
        
        print("\n1. Connecting to database...")
        print(f"   URL: {engine.url}")
        
        print("\n2. Creating tables...")
        create_tables()
        
        print("\n3. Tables created successfully!")
        print("\n   Created tables:")
        for table in Base.metadata.tables.keys():
            print(f"   - {table}")
        
        print("\n" + "=" * 50)
        print("✅ Database setup complete!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Create database: CREATE DATABASE ngoerah_assistant;")
        print("3. Enable pgvector: CREATE EXTENSION vector;")
        print("4. Check .env file for correct DATABASE_URL")
        return False


if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)
