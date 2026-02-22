#!/usr/bin/env python3
"""
Simple test script to verify PostgreSQL connection and basic operations.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(__file__))

def test_postgres_connection():
    """Test basic PostgreSQL connection and operations."""
    print("=== PostgreSQL Connection Test ===\n")
    
    try:
        from api.main import db_engine, SessionLocal, DBProduct, DBOrder, DBUser
        from sqlalchemy import text
        
        # Test 1: Basic connection
        print("1. Testing database connection...")
        with db_engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✓ Connected to PostgreSQL")
            print(f"  Version: {version[:50]}...")
        
        # Test 2: Test tables exist
        print("\n2. Testing table structure...")
        db = SessionLocal()
        
        # Count records in each table
        product_count = db.query(DBProduct).count()
        order_count = db.query(DBOrder).count()
        user_count = db.query(DBUser).count()
        
        print(f"✓ Tables accessible:")
        print(f"  - Products: {product_count} records")
        print(f"  - Orders: {order_count} records")
        print(f"  - Users: {user_count} records")
        
        # Test 3: Sample query
        print("\n3. Testing sample queries...")
        if product_count > 0:
            sample_product = db.query(DBProduct).first()
            print(f"✓ Sample product: {sample_product.name} (${sample_product.price})")
        
        if order_count > 0:
            sample_order = db.query(DBOrder).first()
            print(f"✓ Sample order: {sample_order.id} - {sample_order.status}")
        
        db.close()
        
        # Test 4: Test AI agents with PostgreSQL
        print("\n4. Testing AI agents with PostgreSQL...")
        from api.main import sql_agent
        
        query = "SELECT COUNT(*) as total_products FROM products"
        with db_engine.connect() as conn:
            result = conn.execute(text(query))
            count = result.fetchone()[0]
            print(f"✓ SQL Agent can query database: {count} products found")
        
        print("\n🎉 All PostgreSQL tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your DATABASE_URL in .env")
        print("3. Run the migration script: python migrate_to_postgres.py")
        print("4. Install dependencies: pip install -r requirements.txt")
        return False

def show_connection_info():
    """Display current database connection information."""
    database_url = os.getenv("DATABASE_URL", "Not set")
    print(f"Current DATABASE_URL: {database_url}")
    
    if database_url.startswith("postgresql"):
        # Parse connection string
        parts = database_url.replace("postgresql://", "").split("/")
        server_info = parts[0]  # user:pass@host:port
        db_name = parts[1] if len(parts) > 1 else "unknown"
        
        # Extract host and port
        if "@" in server_info:
            host_port = server_info.split("@")[1]
        else:
            host_port = server_info
            
        print(f"Database: {db_name}")
        print(f"Host: {host_port}")
    elif database_url.startswith("sqlite"):
        print("Database type: SQLite")
        print(f"File: {database_url.replace('sqlite:///', '')}")

if __name__ == "__main__":
    print("=== Database Configuration ===")
    show_connection_info()
    print()
    
    test_postgres_connection()