#!/usr/bin/env python3
"""
Database schema migration script
Updates the database schema to support enhanced product and order data
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./marketplace.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    print("Using SQLite database")
elif DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
    print("Using PostgreSQL database")
else:
    engine = create_engine(DATABASE_URL)
    print(f"Using database: {DATABASE_URL.split('://')[0]}")

def migrate_products_table():
    """Migrate products table to support enhanced data"""
    print("Migrating products table...")
    
    with engine.connect() as conn:
        # Check if columns exist and add them if they don't
        try:
            # Add description column
            conn.execute(text("ALTER TABLE products ADD COLUMN description VARCHAR"))
            print("✅ Added description column to products")
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e).lower():
                print("ℹ️ Description column already exists")
            else:
                print(f"⚠️ Could not add description column: {e}")
        
        try:
            # Add created_date column
            conn.execute(text("ALTER TABLE products ADD COLUMN created_date TIMESTAMP"))
            print("✅ Added created_date column to products")
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e).lower():
                print("ℹ️ Created_date column already exists")
            else:
                print(f"⚠️ Could not add created_date column: {e}")
        
        try:
            # Change price column to FLOAT if it's INTEGER
            conn.execute(text("ALTER TABLE products ALTER COLUMN price TYPE FLOAT"))
            print("✅ Changed price column to FLOAT")
        except Exception as e:
            if "already" in str(e).lower() or "cannot be cast" in str(e).lower():
                print("ℹ️ Price column type is already compatible")
            else:
                print(f"⚠️ Could not change price column type: {e}")
        
        try:
            # Change rating column to FLOAT if it's INTEGER
            conn.execute(text("ALTER TABLE products ALTER COLUMN rating TYPE FLOAT"))
            print("✅ Changed rating column to FLOAT")
        except Exception as e:
            if "already" in str(e).lower() or "cannot be cast" in str(e).lower():
                print("ℹ️ Rating column type is already compatible")
            else:
                print(f"⚠️ Could not change rating column type: {e}")
        
        conn.commit()

def migrate_orders_table():
    """Migrate orders table to support enhanced data"""
    print("Migrating orders table...")
    
    with engine.connect() as conn:
        try:
            # Add customer_name column
            conn.execute(text("ALTER TABLE orders ADD COLUMN customer_name VARCHAR"))
            print("✅ Added customer_name column to orders")
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e).lower():
                print("ℹ️ Customer_name column already exists")
            else:
                print(f"⚠️ Could not add customer_name column: {e}")
        
        try:
            # Add customer_email column
            conn.execute(text("ALTER TABLE orders ADD COLUMN customer_email VARCHAR"))
            print("✅ Added customer_email column to orders")
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e).lower():
                print("ℹ️ Customer_email column already exists")
            else:
                print(f"⚠️ Could not add customer_email column: {e}")
        
        try:
            # Add quantity column
            conn.execute(text("ALTER TABLE orders ADD COLUMN quantity INTEGER"))
            print("✅ Added quantity column to orders")
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e).lower():
                print("ℹ️ Quantity column already exists")
            else:
                print(f"⚠️ Could not add quantity column: {e}")
        
        try:
            # Add created_date column
            conn.execute(text("ALTER TABLE orders ADD COLUMN created_date TIMESTAMP"))
            print("✅ Added created_date column to orders")
        except Exception as e:
            if "already exists" in str(e) or "duplicate column" in str(e).lower():
                print("ℹ️ Created_date column already exists")
            else:
                print(f"⚠️ Could not add created_date column: {e}")
        
        try:
            # Change amount column to FLOAT if it's INTEGER
            conn.execute(text("ALTER TABLE orders ALTER COLUMN amount TYPE FLOAT"))
            print("✅ Changed amount column to FLOAT")
        except Exception as e:
            if "already" in str(e).lower() or "cannot be cast" in str(e).lower():
                print("ℹ️ Amount column type is already compatible")
            else:
                print(f"⚠️ Could not change amount column type: {e}")
        
        conn.commit()

def show_current_schema():
    """Show current database schema"""
    print("\n📊 Current Database Schema:")
    
    with engine.connect() as conn:
        # Show products table schema
        try:
            if DATABASE_URL.startswith("postgresql"):
                result = conn.execute(text("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'products'
                    ORDER BY ordinal_position
                """))
            else:
                result = conn.execute(text("PRAGMA table_info(products)"))
            
            print("\n🛍️ Products Table:")
            for row in result:
                if DATABASE_URL.startswith("postgresql"):
                    print(f"   {row[0]}: {row[1]}")
                else:
                    print(f"   {row[1]}: {row[2]}")
        except Exception as e:
            print(f"⚠️ Could not show products schema: {e}")
        
        # Show orders table schema
        try:
            if DATABASE_URL.startswith("postgresql"):
                result = conn.execute(text("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'orders'
                    ORDER BY ordinal_position
                """))
            else:
                result = conn.execute(text("PRAGMA table_info(orders)"))
            
            print("\n📦 Orders Table:")
            for row in result:
                if DATABASE_URL.startswith("postgresql"):
                    print(f"   {row[0]}: {row[1]}")
                else:
                    print(f"   {row[1]}: {row[2]}")
        except Exception as e:
            print(f"⚠️ Could not show orders schema: {e}")

def main():
    """Main migration function"""
    print("🔄 Starting Database Schema Migration...")
    print(f"Database: {DATABASE_URL}")
    
    try:
        # Show current schema
        show_current_schema()
        
        # Migrate tables
        migrate_products_table()
        migrate_orders_table()
        
        # Show updated schema
        show_current_schema()
        
        print("\n🎉 Database migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")

if __name__ == "__main__":
    main()