#!/usr/bin/env python3
"""
Database verification script
Shows sample data from the seeded database
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./marketplace.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
elif DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def show_sample_products():
    """Show sample products from each category"""
    print("🛍️ Sample Products by Category:")
    
    with engine.connect() as conn:
        # Get sample products from each category
        result = conn.execute(text("""
            SELECT DISTINCT category FROM products ORDER BY category
        """))
        
        categories = [row[0] for row in result]
        
        for category in categories:
            result = conn.execute(text("""
                SELECT name, price, stock, seller, rating 
                FROM products 
                WHERE category = :category 
                ORDER BY rating DESC 
                LIMIT 3
            """), {"category": category})
            
            print(f"\n📂 {category}:")
            for row in result:
                name, price, stock, seller, rating = row
                print(f"   • {name}")
                print(f"     Price: {price} ብር | Stock: {stock} | Seller: {seller} | Rating: {rating}⭐")

def show_sample_orders():
    """Show sample orders"""
    print("\n📦 Sample Recent Orders:")
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, product, amount, status, customer_name, quantity, date
            FROM orders 
            ORDER BY created_date DESC 
            LIMIT 10
        """))
        
        for row in result:
            order_id, product, amount, status, customer, quantity, date = row
            print(f"\n🧾 Order {order_id}")
            print(f"   Customer: {customer}")
            print(f"   Product: {product}")
            print(f"   Quantity: {quantity} | Amount: {amount} ብር")
            print(f"   Status: {status} | Date: {date}")

def show_statistics():
    """Show database statistics"""
    print("\n📊 Database Statistics:")
    
    with engine.connect() as conn:
        # Product statistics
        result = conn.execute(text("SELECT COUNT(*) FROM products")).fetchone()
        print(f"   Total Products: {result[0]}")
        
        result = conn.execute(text("SELECT COUNT(*) FROM orders")).fetchone()
        print(f"   Total Orders: {result[0]}")
        
        # Price range
        result = conn.execute(text("SELECT MIN(price), MAX(price), AVG(price) FROM products")).fetchone()
        min_price, max_price, avg_price = result
        print(f"   Price Range: {min_price:.2f} - {max_price:.2f} ብር (Avg: {avg_price:.2f} ብር)")
        
        # Top categories by product count
        print(f"\n📈 Top Product Categories:")
        result = conn.execute(text("""
            SELECT category, COUNT(*) as count 
            FROM products 
            GROUP BY category 
            ORDER BY count DESC 
            LIMIT 5
        """))
        
        for category, count in result:
            print(f"   {category}: {count} products")
        
        # Order status distribution
        print(f"\n📦 Order Status Distribution:")
        result = conn.execute(text("""
            SELECT status, COUNT(*) as count 
            FROM orders 
            GROUP BY status 
            ORDER BY count DESC
        """))
        
        for status, count in result:
            print(f"   {status}: {count} orders")
        
        # Top sellers
        print(f"\n🏪 Top Sellers by Product Count:")
        result = conn.execute(text("""
            SELECT seller, COUNT(*) as count 
            FROM products 
            GROUP BY seller 
            ORDER BY count DESC 
            LIMIT 5
        """))
        
        for seller, count in result:
            print(f"   {seller}: {count} products")

def main():
    """Main verification function"""
    print("🔍 Ethiopian Marketplace Database Verification")
    print(f"Database: {DATABASE_URL}")
    print("=" * 60)
    
    try:
        show_statistics()
        show_sample_products()
        show_sample_orders()
        
        print("\n" + "=" * 60)
        print("✅ Database verification completed successfully!")
        print("🎯 The database is ready for use with realistic Ethiopian marketplace data!")
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")

if __name__ == "__main__":
    main()