#!/usr/bin/env python3
"""
Database seeding script for Ethiopian Marketplace
Creates 200-300 products and orders with realistic data
"""

import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class DBProduct(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    category = Column(String)
    seller = Column(String)
    rating = Column(Float)
    description = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow)

class DBOrder(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    product = Column(String)
    amount = Column(Float)
    status = Column(String)
    date = Column(String)
    customer_name = Column(String)
    customer_email = Column(String)
    quantity = Column(Integer)
    created_date = Column(DateTime, default=datetime.utcnow)

# Ethiopian marketplace product data
ETHIOPIAN_PRODUCTS = [
    # Grains & Cereals
    {"name": "Premium Teff Flour", "category": "Grains", "base_price": 45.0, "description": "High-quality white teff flour from Debre Zeit"},
    {"name": "Red Teff Flour", "category": "Grains", "base_price": 42.0, "description": "Traditional red teff flour, rich in iron"},
    {"name": "Mixed Teff Flour", "category": "Grains", "base_price": 40.0, "description": "Blend of white and red teff flour"},
    {"name": "Barley Flour", "category": "Grains", "base_price": 25.0, "description": "Fresh ground barley flour from Arsi"},
    {"name": "Wheat Flour", "category": "Grains", "base_price": 30.0, "description": "Premium wheat flour for bread making"},
    {"name": "Sorghum Grain", "category": "Grains", "base_price": 22.0, "description": "Drought-resistant sorghum from Tigray"},
    {"name": "Millet Seeds", "category": "Grains", "base_price": 28.0, "description": "Nutritious finger millet from SNNPR"},
    {"name": "Quinoa Seeds", "category": "Grains", "base_price": 85.0, "description": "Organic quinoa grown in Ethiopian highlands"},
    
    # Coffee & Beverages
    {"name": "Yirgacheffe Coffee Beans", "category": "Coffee", "base_price": 65.0, "description": "Single origin coffee from Yirgacheffe region"},
    {"name": "Sidamo Coffee Beans", "category": "Coffee", "base_price": 60.0, "description": "Premium Sidamo coffee with floral notes"},
    {"name": "Harar Coffee Beans", "category": "Coffee", "base_price": 58.0, "description": "Traditional Harar coffee with wine-like flavor"},
    {"name": "Limu Coffee Beans", "category": "Coffee", "base_price": 55.0, "description": "Mild and balanced Limu coffee"},
    {"name": "Green Coffee Beans", "category": "Coffee", "base_price": 45.0, "description": "Unroasted green coffee beans for home roasting"},
    {"name": "Ethiopian Honey Wine", "category": "Beverages", "base_price": 120.0, "description": "Traditional tej honey wine"},
    {"name": "Gesho Leaves", "category": "Beverages", "base_price": 15.0, "description": "Dried gesho leaves for brewing tej"},
    {"name": "Herbal Tea Mix", "category": "Beverages", "base_price": 25.0, "description": "Traditional Ethiopian herbal tea blend"},
    
    # Spices & Seasonings
    {"name": "Berbere Spice Mix", "category": "Spices", "base_price": 35.0, "description": "Authentic Ethiopian berbere spice blend"},
    {"name": "Mitmita Spice", "category": "Spices", "base_price": 40.0, "description": "Hot and spicy mitmita powder"},
    {"name": "Korarima Seeds", "category": "Spices", "base_price": 180.0, "description": "Ethiopian cardamom seeds"},
    {"name": "Fenugreek Seeds", "category": "Spices", "base_price": 22.0, "description": "Aromatic fenugreek seeds"},
    {"name": "Nigella Seeds", "category": "Spices", "base_price": 28.0, "description": "Black cumin seeds with medicinal properties"},
    {"name": "Turmeric Powder", "category": "Spices", "base_price": 32.0, "description": "Fresh ground turmeric from local farms"},
    {"name": "Coriander Seeds", "category": "Spices", "base_price": 18.0, "description": "Whole coriander seeds"},
    {"name": "Ethiopian Mustard Seeds", "category": "Spices", "base_price": 25.0, "description": "Local variety mustard seeds"},
    
    # Natural Foods & Honey
    {"name": "White Honey", "category": "Natural Foods", "base_price": 85.0, "description": "Pure white honey from Tigray highlands"},
    {"name": "Forest Honey", "category": "Natural Foods", "base_price": 75.0, "description": "Wild forest honey with complex flavors"},
    {"name": "Sunflower Honey", "category": "Natural Foods", "base_price": 65.0, "description": "Light colored sunflower honey"},
    {"name": "Eucalyptus Honey", "category": "Natural Foods", "base_price": 70.0, "description": "Medicinal eucalyptus honey"},
    {"name": "Beeswax", "category": "Natural Foods", "base_price": 45.0, "description": "Pure beeswax for cosmetics and candles"},
    {"name": "Royal Jelly", "category": "Natural Foods", "base_price": 250.0, "description": "Fresh royal jelly with health benefits"},
    {"name": "Propolis Extract", "category": "Natural Foods", "base_price": 120.0, "description": "Natural propolis for immune support"},
    
    # Oils & Fats
    {"name": "Nug Oil", "category": "Oils", "base_price": 55.0, "description": "Cold-pressed niger seed oil"},
    {"name": "Sunflower Oil", "category": "Oils", "base_price": 48.0, "description": "Refined sunflower cooking oil"},
    {"name": "Sesame Oil", "category": "Oils", "base_price": 65.0, "description": "Traditional sesame seed oil"},
    {"name": "Linseed Oil", "category": "Oils", "base_price": 42.0, "description": "Cold-pressed flax seed oil"},
    {"name": "Coconut Oil", "category": "Oils", "base_price": 78.0, "description": "Virgin coconut oil"},
    {"name": "Shea Butter", "category": "Oils", "base_price": 95.0, "description": "Raw shea butter for cosmetics"},
    
    # Legumes & Pulses
    {"name": "Red Lentils", "category": "Legumes", "base_price": 35.0, "description": "Split red lentils for misr wot"},
    {"name": "Yellow Split Peas", "category": "Legumes", "base_price": 32.0, "description": "Yellow split peas for kik alicha"},
    {"name": "Chickpeas", "category": "Legumes", "base_price": 38.0, "description": "Whole chickpeas from Shewa"},
    {"name": "Black Beans", "category": "Legumes", "base_price": 42.0, "description": "Ethiopian black beans"},
    {"name": "White Beans", "category": "Legumes", "base_price": 40.0, "description": "Large white beans for stews"},
    {"name": "Fava Beans", "category": "Legumes", "base_price": 36.0, "description": "Dried fava beans"},
    {"name": "Green Lentils", "category": "Legumes", "base_price": 38.0, "description": "Whole green lentils"},
    
    # Vegetables & Fruits
    {"name": "Dried Tomatoes", "category": "Vegetables", "base_price": 45.0, "description": "Sun-dried tomatoes from Rift Valley"},
    {"name": "Dried Onions", "category": "Vegetables", "base_price": 28.0, "description": "Dehydrated onion flakes"},
    {"name": "Dried Peppers", "category": "Vegetables", "base_price": 35.0, "description": "Dried hot peppers for berbere"},
    {"name": "Moringa Powder", "category": "Vegetables", "base_price": 65.0, "description": "Nutritious moringa leaf powder"},
    {"name": "Baobab Fruit Powder", "category": "Fruits", "base_price": 85.0, "description": "Vitamin C rich baobab powder"},
    {"name": "Tamarind Paste", "category": "Fruits", "base_price": 32.0, "description": "Sour tamarind paste"},
    
    # Handicrafts & Traditional Items
    {"name": "Handwoven Basket", "category": "Crafts", "base_price": 125.0, "description": "Traditional Ethiopian basket"},
    {"name": "Coffee Ceremony Set", "category": "Crafts", "base_price": 180.0, "description": "Complete coffee ceremony equipment"},
    {"name": "Clay Coffee Pot", "category": "Crafts", "base_price": 45.0, "description": "Traditional jebena for coffee"},
    {"name": "Bamboo Products", "category": "Crafts", "base_price": 65.0, "description": "Handmade bamboo household items"},
    {"name": "Leather Goods", "category": "Crafts", "base_price": 95.0, "description": "Traditional leather products"},
    {"name": "Wooden Utensils", "category": "Crafts", "base_price": 35.0, "description": "Hand-carved wooden kitchen tools"},
    {"name": "Traditional Textiles", "category": "Crafts", "base_price": 150.0, "description": "Handwoven Ethiopian textiles"},
    {"name": "Incense Burner", "category": "Crafts", "base_price": 55.0, "description": "Traditional clay incense burner"},
    
    # Health & Wellness
    {"name": "Ethiopian Black Seed", "category": "Health", "base_price": 48.0, "description": "Nigella sativa seeds for health"},
    {"name": "Medicinal Herbs Mix", "category": "Health", "base_price": 42.0, "description": "Traditional medicinal herb blend"},
    {"name": "Aloe Vera Gel", "category": "Health", "base_price": 35.0, "description": "Pure aloe vera gel"},
    {"name": "Frankincense Resin", "category": "Health", "base_price": 120.0, "description": "Premium frankincense from Tigray"},
    {"name": "Myrrh Resin", "category": "Health", "base_price": 95.0, "description": "Natural myrrh resin"},
    {"name": "Ethiopian Tea", "category": "Health", "base_price": 28.0, "description": "Herbal tea for wellness"},
]

ETHIOPIAN_SELLERS = [
    "Addis Organic Farm", "Habesha Spices Co", "Yirgacheffe Coffee Coop", "Tigray Honey Producers",
    "Shewa Grain Traders", "Arsi Barley Farm", "SNNPR Millet Coop", "Oromia Coffee Union",
    "Sidamo Coffee Growers", "Harar Coffee Collective", "Limu Coffee Association", "Gedeo Coffee Farm",
    "Amhara Honey Collective", "Wollo Spice Traders", "Gojjam Grain Market", "Bahir Dar Organics",
    "Debre Zeit Teff Farm", "Adama Spice House", "Jimma Coffee Estate", "Nekemte Coffee Farm",
    "Dire Dawa Traders", "Awash Valley Farm", "Rift Valley Organics", "Highland Honey Co",
    "Ethiopian Spice Masters", "Abyssinian Traders", "Blue Nile Organics", "Red Sea Spices",
    "Mountain View Farm", "Valley Fresh Produce", "Desert Rose Traders", "Green Hills Organic",
    "Golden Grain Co", "Sunrise Spices", "Moonlight Honey", "Star Coffee Roasters",
    "Eagle Spice Trading", "Lion Coffee Estate", "Zebra Organic Farm", "Giraffe Grain Co",
    "Elephant Spice House", "Rhino Coffee Traders", "Hippo Honey Farm", "Crocodile Crafts",
    "Cheetah Coffee Co", "Leopard Spice Mix", "Hyena Grain Market", "Baboon Organic Farm"
]

ETHIOPIAN_CUSTOMERS = [
    "Abebe Kebede", "Almaz Tadesse", "Bereket Haile", "Chaltu Bekele", "Dawit Mekonnen",
    "Emebet Girma", "Fikadu Wolde", "Genet Assefa", "Hailu Tesfaye", "Iyasu Negash",
    "Jember Alemu", "Kalkidan Desta", "Lemlem Yohannes", "Meron Getachew", "Nardos Mulugeta",
    "Olana Regassa", "Peniel Teshome", "Rahel Solomon", "Selamawit Abera", "Tadesse Worku",
    "Urael Kidane", "Veronica Tekle", "Wondwossen Ayele", "Yared Shiferaw", "Zara Mengistu",
    "Amanuel Gebre", "Bethlehem Fekadu", "Chala Gemechu", "Desta Legesse", "Eyob Tilahun",
    "Frehiwot Berhane", "Girma Tadele", "Hanan Abdella", "Ibrahim Seid", "Jemal Hussein",
    "Kidist Mulatu", "Liya Demissie", "Mahlet Taye", "Natnael Worku", "Obsie Regassa",
    "Paulos Gebru", "Qedest Hailu", "Robel Tefera", "Saron Bekele", "Tewodros Alemu",
    "Uzma Ahmed", "Violet Tekeste", "Wubit Kassahun", "Yonas Berhe", "Zelalem Tadesse"
]

ORDER_STATUSES = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
STATUS_WEIGHTS = [0.15, 0.20, 0.25, 0.35, 0.05]  # More delivered orders

def generate_email(name):
    """Generate email from Ethiopian name"""
    parts = name.lower().split()
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}@gmail.com"
    return f"{parts[0]}@gmail.com"

def generate_order_id():
    """Generate Ethiopian-style order ID"""
    prefixes = ["ETH", "ADD", "ORO", "AMH", "TIG", "SNN", "SOM", "HAR"]
    return f"{random.choice(prefixes)}-{random.randint(1000, 9999)}"

def create_products(session, num_products=250):
    """Create realistic Ethiopian marketplace products"""
    print(f"Creating {num_products} products...")
    
    products_created = 0
    
    # Create multiple variants of each base product
    for base_product in ETHIOPIAN_PRODUCTS:
        if products_created >= num_products:
            break
            
        # Create 3-5 variants of each product
        variants = random.randint(3, 5)
        for i in range(variants):
            if products_created >= num_products:
                break
                
            # Add size/weight variations to name
            sizes = ["500g", "1kg", "2kg", "5kg", "250ml", "500ml", "1L", "Small", "Medium", "Large"]
            size = random.choice(sizes)
            
            # Price variation based on size and quality
            price_multiplier = random.uniform(0.8, 1.5)
            if "Large" in size or "5kg" in size or "2kg" in size:
                price_multiplier *= 1.3
            elif "Small" in size or "250ml" in size or "500g" in size:
                price_multiplier *= 0.7
                
            product = DBProduct(
                name=f"{base_product['name']} ({size})",
                price=round(base_product['base_price'] * price_multiplier, 2),
                stock=random.randint(5, 200),
                category=base_product['category'],
                seller=random.choice(ETHIOPIAN_SELLERS),
                rating=round(random.uniform(3.5, 5.0), 1),
                description=base_product['description'],
                created_date=datetime.now() - timedelta(days=random.randint(1, 365))
            )
            
            session.add(product)
            products_created += 1
            
            if products_created % 50 == 0:
                print(f"Created {products_created} products...")
    
    session.commit()
    print(f"✅ Created {products_created} products")
    return products_created

def create_orders(session, num_orders=280):
    """Create realistic Ethiopian marketplace orders"""
    print(f"Creating {num_orders} orders...")
    
    # Get all products for order creation
    products = session.query(DBProduct).all()
    if not products:
        print("❌ No products found. Create products first.")
        return 0
    
    orders_created = 0
    
    for i in range(num_orders):
        product = random.choice(products)
        customer = random.choice(ETHIOPIAN_CUSTOMERS)
        quantity = random.randint(1, 5)
        
        # Calculate total amount
        total_amount = round(product.price * quantity, 2)
        
        # Generate order date (last 6 months)
        order_date = datetime.now() - timedelta(days=random.randint(1, 180))
        
        order = DBOrder(
            id=generate_order_id(),
            product=product.name,
            amount=total_amount,
            status=random.choices(ORDER_STATUSES, weights=STATUS_WEIGHTS)[0],
            date=order_date.strftime("%Y-%m-%d"),
            customer_name=customer,
            customer_email=generate_email(customer),
            quantity=quantity,
            created_date=order_date
        )
        
        session.add(order)
        orders_created += 1
        
        if orders_created % 50 == 0:
            print(f"Created {orders_created} orders...")
    
    session.commit()
    print(f"✅ Created {orders_created} orders")
    return orders_created

def clear_existing_data(session):
    """Clear existing products and orders"""
    print("Clearing existing data...")
    session.execute(text("DELETE FROM orders"))
    session.execute(text("DELETE FROM products"))
    session.commit()
    print("✅ Cleared existing data")

def main():
    """Main seeding function"""
    print("🌱 Starting Ethiopian Marketplace Database Seeding...")
    print(f"Database: {DATABASE_URL}")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = SessionLocal()
    
    try:
        # Clear existing data
        clear_existing_data(session)
        
        # Create products (250 products)
        products_count = create_products(session, 250)
        
        # Create orders (280 orders)
        orders_count = create_orders(session, 280)
        
        print("\n🎉 Database seeding completed successfully!")
        print(f"📊 Summary:")
        print(f"   Products created: {products_count}")
        print(f"   Orders created: {orders_count}")
        print(f"   Total records: {products_count + orders_count}")
        
        # Show some statistics
        print(f"\n📈 Statistics:")
        categories = session.execute(text("SELECT category, COUNT(*) as count FROM products GROUP BY category")).fetchall()
        for category, count in categories:
            print(f"   {category}: {count} products")
            
        statuses = session.execute(text("SELECT status, COUNT(*) as count FROM orders GROUP BY status")).fetchall()
        print(f"\n📦 Order Status Distribution:")
        for status, count in statuses:
            print(f"   {status}: {count} orders")
            
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()