#!/usr/bin/env python3
"""
Migration script to move from SQLite to PostgreSQL.
This script will:
1. Create all tables in PostgreSQL
2. Migrate existing data from SQLite (if it exists)
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

# Load environment variables
load_dotenv()

# Define models here to avoid import issues
Base = declarative_base()

class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class DBProduct(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    stock = Column(Integer)
    category = Column(String)
    seller = Column(String)
    rating = Column(Integer)

class DBOrder(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    product = Column(String)
    amount = Column(Integer)
    status = Column(String)
    date = Column(String)

def migrate_data():
    """Migrate data from SQLite to PostgreSQL."""
    sqlite_url = "sqlite:///./marketplace.db"
    postgres_url = os.getenv("DATABASE_URL")
    
    # Check if SQLite database exists
    if not os.path.exists("marketplace.db"):
        print("No SQLite database found. Creating fresh PostgreSQL database with sample data.")
        create_sample_data()
        return True
    
    try:
        # Connect to both databases
        sqlite_engine = create_engine(sqlite_url)
        postgres_engine = create_engine(postgres_url)
        
        # Create tables in PostgreSQL
        Base.metadata.create_all(bind=postgres_engine)
        print("✓ Created tables in PostgreSQL")
        
        # Create sessions
        SqliteSession = sessionmaker(bind=sqlite_engine)
        PostgresSession = sessionmaker(bind=postgres_engine)
        
        sqlite_session = SqliteSession()
        postgres_session = PostgresSession()
        
        # Migrate Users
        users = sqlite_session.query(DBUser).all()
        for user in users:
            new_user = DBUser(
                id=user.id,
                name=user.name,
                email=user.email,
                hashed_password=user.hashed_password
            )
            postgres_session.merge(new_user)
        print(f"✓ Migrated {len(users)} users")
        
        # Migrate Products
        products = sqlite_session.query(DBProduct).all()
        for product in products:
            new_product = DBProduct(
                id=product.id,
                name=product.name,
                price=product.price,
                stock=product.stock,
                category=product.category,
                seller=product.seller,
                rating=getattr(product, 'rating', 4)  # Default rating if not exists
            )
            postgres_session.merge(new_product)
        print(f"✓ Migrated {len(products)} products")
        
        # Migrate Orders
        orders = sqlite_session.query(DBOrder).all()
        for order in orders:
            new_order = DBOrder(
                id=order.id,
                product=order.product,
                amount=order.amount,
                status=order.status,
                date=order.date
            )
            postgres_session.merge(new_order)
        print(f"✓ Migrated {len(orders)} orders")
        
        # Commit changes
        postgres_session.commit()
        
        # Close sessions
        sqlite_session.close()
        postgres_session.close()
        
        print("✓ Data migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during migration: {e}")
        return False

def create_sample_data():
    """Create sample data in PostgreSQL."""
    postgres_url = os.getenv("DATABASE_URL")
    postgres_engine = create_engine(postgres_url)
    
    # Create tables
    Base.metadata.create_all(bind=postgres_engine)
    print("✓ Created tables in PostgreSQL")
    
    # Create session
    PostgresSession = sessionmaker(bind=postgres_engine)
    postgres_session = PostgresSession()
    
    # Sample products
    sample_products = [
        {"id": 1, "name": "Premium Teff Flour (5kg)", "price": 45, "stock": 120, "category": "Grains", "seller": "Adane Farms", "rating": 4},
        {"id": 2, "name": "Organic Honey (500g)", "price": 12, "stock": 45, "category": "Natural Foods", "seller": "Zewditu Honey", "rating": 4},
        {"id": 3, "name": "Cold Pressed Linseed Oil", "price": 8, "stock": 15, "category": "Oils", "seller": "EthioOil", "rating": 4},
        {"id": 4, "name": "Green Coffee Beans (1kg)", "price": 18, "stock": 200, "category": "Coffee", "seller": "Yirgacheffe Coop", "rating": 4},
        {"id": 5, "name": "Handmade Bamboo Basket", "price": 25, "stock": 8, "category": "Crafts", "seller": "Arba Minch Crafts", "rating": 4},
    ]
    
    for p in sample_products:
        product = DBProduct(**p)
        postgres_session.merge(product)
    
    # Sample orders
    sample_orders = [
        {"id": "ORD-101", "product": "Premium Teff Flour", "amount": 45, "status": "Delivered", "date": "2024-03-10"},
        {"id": "ORD-102", "product": "Organic Honey", "amount": 25, "status": "Shipped", "date": "2024-03-11"},
        {"id": "ORD-103", "product": "Green Coffee Beans", "amount": 180, "status": "Pending", "date": "2024-03-12"},
    ]
    
    for o in sample_orders:
        order = DBOrder(**o)
        postgres_session.merge(order)
    
    postgres_session.commit()
    postgres_session.close()
    
    print("✓ Created sample data in PostgreSQL")

def test_connection():
    """Test the PostgreSQL connection."""
    try:
        postgres_url = os.getenv("DATABASE_URL")
        engine = create_engine(postgres_url)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✓ PostgreSQL connection successful!")
            print(f"  Version: {version}")
        
        # Test with the models
        PostgresSession = sessionmaker(bind=engine)
        db = PostgresSession()
        products = db.query(DBProduct).count()
        orders = db.query(DBOrder).count()
        users = db.query(DBUser).count()
        db.close()
        
        print(f"✓ Database contains:")
        print(f"  - {products} products")
        print(f"  - {orders} orders") 
        print(f"  - {users} users")
        
        return True
    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        return False

def main():
    print("=== PostgreSQL Migration Script ===\n")
    
    # Step 1: Migrate data
    print("Step 1: Setting up PostgreSQL and migrating data...")
    if not migrate_data():
        return
    
    # Step 2: Test connection
    print("\nStep 2: Testing connection...")
    if not test_connection():
        return
    
    print("\n🎉 Migration completed successfully!")
    print("\nNext steps:")
    print("1. Your PostgreSQL database is ready!")
    print("2. Restart your application to use PostgreSQL")
    print("3. All AI agents will work with the new database")

if __name__ == "__main__":
    main()