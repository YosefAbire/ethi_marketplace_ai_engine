import os
from dotenv import load_dotenv

# Load environment variables from .env file FIRST
# Handle both direct execution and import from parent directory
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()  # Try current directory

from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import json
import shutil
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext

from agents.rag_agent import RAGAgent
from agents.workflow_agent import WorkflowAgent
from agents.sql_agent import SQLAgent
from agents.seller_agent import SellerAgent
from agents.ops_agent import OpsAgent
from agents.recommendation_agent import RecommendationAgent
from agents.fraud_detection_agent import FraudDetectionAgent
from services.fraud_detection_service import FraudDetectionService
from services.email_service import EmailService
from .firebase_auth import get_current_user

app = FastAPI(title="Ethi Marketplace AI Engine")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Temporarily broad for debugging 400 error
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# --- Mock Data for Simulation ---
MOCK_PRODUCTS = [
    {"id": 1, "name": "Premium Teff Flour (5kg)", "price": 45.0, "stock": 120, "category": "Grains", "seller": "Adane Farms", "rating": 4.9},
    {"id": 2, "name": "Organic Honey (500g)", "price": 12.5, "stock": 45, "category": "Natural Foods", "seller": "Zewditu Honey", "rating": 4.7},
    {"id": 3, "name": "Cold Pressed Linseed Oil", "price": 8.0, "stock": 15, "category": "Oils", "seller": "EthioOil", "rating": 4.5},
    {"id": 4, "name": "Green Coffee Beans (1kg)", "price": 18.0, "stock": 200, "category": "Coffee", "seller": "Yirgacheffe Coop", "rating": 4.9},
    {"id": 5, "name": "Handmade Bamboo Basket", "price": 25.0, "stock": 8, "category": "Crafts", "seller": "Arba Minch Crafts", "rating": 4.8},
]

MOCK_ORDERS = [
    {"id": "ORD-101", "product": "Premium Teff Flour", "amount": 45.0, "status": 'Delivered', "date": '2024-03-10'},
    {"id": "ORD-102", "product": "Organic Honey", "amount": 25.0, "status": 'Shipped', "date": '2024-03-11'},
    {"id": "ORD-103", "product": "Green Coffee Beans", "amount": 180.0, "status": 'Pending', "date": '2024-03-12'},
]

# --- Database & Auth Setup ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./marketplace.db")

# Create engine with appropriate settings for different databases
if DATABASE_URL.startswith("sqlite"):
    db_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    print("Using SQLite database")
elif DATABASE_URL.startswith("postgresql"):
    db_engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
    print("Using PostgreSQL database")
else:
    db_engine = create_engine(DATABASE_URL)
    print(f"Using database: {DATABASE_URL.split('://')[0]}")
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
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
    rating = Column(Integer)

class DBOrder(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    product = Column(String)
    amount = Column(Integer)
    status = Column(String)
    date = Column(String)

Base.metadata.create_all(bind=db_engine)

# Seed Function
def seed_db():
    db = SessionLocal()
    if db.query(DBProduct).count() == 0:
        for p in MOCK_PRODUCTS:
            db.add(DBProduct(name=p["name"], price=int(p["price"]), stock=p["stock"], category=p["category"], seller=p["seller"], rating=int(p["rating"])))
        for o in MOCK_ORDERS:
            db.add(DBOrder(id=o["id"], product=o["product"], amount=int(o["amount"]), status=o["status"], date=o["date"]))
        db.commit()
    db.close()

seed_db()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Agent Initialization ---

# Global instances
def get_market_snapshot():
    db = SessionLocal()
    products = db.query(DBProduct).all()
    orders = db.query(DBOrder).all()
    db.close()
    
    products_list = [{"name": p.name, "price": p.price, "stock": p.stock, "category": p.category} for p in products]
    orders_list = [{"product": o.product, "amount": o.amount, "status": o.status} for o in orders]
    
    return f"PRODUCTS:\n{json.dumps(products_list, indent=2)}\n\nRECENT ORDERS:\n{json.dumps(orders_list, indent=2)}"

# Initialize agents with proper error handling
def initialize_agents():
    global sql_agent, workflow_agent, rag_agent, seller_agent, ops_agent, recommendation_agent, fraud_detection_service
    
    # SQL Agent (always works)
    sql_agent = SQLAgent(db_engine=db_engine)
    
    # Initialize Workflow Agent
    try:
        workflow_agent = WorkflowAgent()
        print("Workflow Agent initialized successfully")
    except Exception as e:
        print(f"Workflow Agent Init Error: {e}")
        workflow_agent = None

    # Initialize RAG Agent lazily to allow recovery from startup errors (like quota exhausted)
    rag_agent = None
    try:
        print("Attempting to initialize RAG Agent...")
        rag_agent = RAGAgent(data_dir="./data", persist_dir="./chroma_db")
        print("RAG Agent initialized successfully")
    except Exception as e:
        print(f"RAG Agent Initialization Error: {e}")

    # Initialize Seller Agent
    try:
        seller_agent = SellerAgent()
        print("Seller Agent initialized successfully")
    except Exception as e:
        print(f"Seller Agent Init Error: {e}")
        seller_agent = None

    # Initialize Operations Agent
    try:
        ops_agent = OpsAgent()
        print("Operations Agent initialized successfully")
    except Exception as e:
        print(f"Operations Agent Init Error: {e}")
        ops_agent = None

    # Initialize Recommendation Agent
    try:
        recommendation_agent = RecommendationAgent(
            sql_agent=sql_agent,
            rag_agent=rag_agent  # May be None if RAG failed to init
        )
        print("Recommendation Agent initialized successfully")
    except Exception as e:
        print(f"Recommendation Agent Init Error: {e}")
        recommendation_agent = None

    # Initialize Fraud Detection Service
    try:
        fraud_detection_service = FraudDetectionService(
            db_engine=db_engine,
            sql_agent=sql_agent,
            rag_agent=rag_agent
        )
        print("Fraud Detection Service initialized successfully")
    except Exception as e:
        print(f"Fraud Detection Service Init Error: {e}")
        fraud_detection_service = None

# Initialize all agents
initialize_agents()

class Query(BaseModel):
    prompt: str
    user_id: Optional[str] = "system"

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.get("/")
async def root():
    return {"status": "online", "version": "1.5.0"}

@app.post("/register")
async def register(user: UserCreate):
    db = SessionLocal()
    db_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if db_user:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = DBUser(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    
    return {
        "name": new_user.name,
        "email": new_user.email,
        "token": f"auth-token-{new_user.id}" # Simplified token
    }

@app.post("/login")
async def login(user: UserLogin):
    db = SessionLocal()
    db_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        db.close()
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    db.close()
    return {
        "name": db_user.name,
        "email": db_user.email,
        "token": f"auth-token-{db_user.id}"
    }

@app.get("/auth/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Return the currently authenticated Firebase user."""
    return current_user

# --- Dashboard Endpoints (Protected) ---
@app.get("/dashboard/stats")
async def get_dashboard_stats(current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    products = db.query(DBProduct).all()
    orders = db.query(DBOrder).all()
    
    total_revenue = sum(o.amount for o in orders)
    active_orders = len([o for o in orders if o.status != 'Delivered'])
    inventory_count = len(products)
    alerts_count = len([p for p in products if p.stock < 20])
    
    db.close()
    return {
        "totalRevenue": total_revenue,
        "activeOrders": active_orders,
        "inventoryCount": inventory_count,
        "alertsCount": alerts_count
    }

@app.get("/dashboard/products")
async def get_all_products(current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    products = db.query(DBProduct).all()
    db.close()
    return products

@app.get("/dashboard/orders")
async def get_all_orders(current_user: dict = Depends(get_current_user)):
    db = SessionLocal()
    orders = db.query(DBOrder).all()
    db.close()
    return orders

@app.get("/dashboard/analytics")
async def get_analytics(current_user: dict = Depends(get_current_user)):
    """Analytics endpoint for dashboard charts and insights."""
    try:
        db = SessionLocal()
        products = db.query(DBProduct).all()
        orders = db.query(DBOrder).all()
        db.close()
        
        # Generate mock analytics data based on actual database content
        analytics_data = {
            "source": "database",
            "gender_distribution": [
                {"name": "Male", "value": 45},
                {"name": "Female", "value": 55}
            ],
            "age_distribution": [
                {"name": "18-25", "count": 120},
                {"name": "26-35", "count": 180},
                {"name": "36-45", "count": 150},
                {"name": "46-55", "count": 90},
                {"name": "55+", "count": 60}
            ],
            "spending_vs_income": [
                {"x": 20, "y": 30}, {"x": 25, "y": 45}, {"x": 30, "y": 55},
                {"x": 35, "y": 65}, {"x": 40, "y": 70}, {"x": 45, "y": 75},
                {"x": 50, "y": 80}, {"x": 55, "y": 85}, {"x": 60, "y": 90},
                {"x": 65, "y": 85}, {"x": 70, "y": 80}, {"x": 75, "y": 75}
            ],
            "category_performance": {},
            "revenue_trends": {},
            "total_customers": 600,
            "total_transactions": len(orders),
            "avg_order_value": sum(o.amount for o in orders) / len(orders) if orders else 0
        }
        
        # Add category performance based on actual products
        category_counts = {}
        for product in products:
            category = product.category
            if category not in category_counts:
                category_counts[category] = {"count": 0, "total_value": 0}
            category_counts[category]["count"] += 1
            category_counts[category]["total_value"] += product.price * product.stock
        
        analytics_data["category_performance"] = category_counts
        
        # Add revenue trends based on actual orders
        revenue_by_date = {}
        for order in orders:
            date = order.date
            if date not in revenue_by_date:
                revenue_by_date[date] = 0
            revenue_by_date[date] += order.amount
        
        analytics_data["revenue_trends"] = [
            {"date": date, "revenue": revenue} 
            for date, revenue in sorted(revenue_by_date.items())
        ]
        
        return analytics_data
        
    except Exception as e:
        print(f"Analytics error: {e}")
        # Return mock data if database fails
        return {
            "source": "mock",
            "gender_distribution": [
                {"name": "Male", "value": 45},
                {"name": "Female", "value": 55}
            ],
            "age_distribution": [
                {"name": "18-25", "count": 120},
                {"name": "26-35", "count": 180},
                {"name": "36-45", "count": 150},
                {"name": "46-55", "count": 90},
                {"name": "55+", "count": 60}
            ],
            "spending_vs_income": [
                {"x": 20, "y": 30}, {"x": 25, "y": 45}, {"x": 30, "y": 55},
                {"x": 35, "y": 65}, {"x": 40, "y": 70}, {"x": 45, "y": 75},
                {"x": 50, "y": 80}, {"x": 55, "y": 85}, {"x": 60, "y": 90}
            ],
            "total_customers": 600,
            "total_transactions": 150,
            "avg_order_value": 45.50
        }

@app.get("/dashboard/search")
async def search_dashboard(q: str = "", current_user: dict = Depends(get_current_user)):
    """Enhanced search endpoint for dashboard data."""
    if not q.strip():
        return {"results": [], "total": 0, "query": q}
    
    try:
        db = SessionLocal()
        products = db.query(DBProduct).all()
        orders = db.query(DBOrder).all()
        db.close()
        
        query_lower = q.lower()
        results = []
        
        # Search products
        for product in products:
            if (query_lower in product.name.lower() or 
                query_lower in product.category.lower() or 
                query_lower in product.seller.lower() or
                query_lower in str(product.price) or
                query_lower in str(product.stock)):
                results.append({
                    "type": "product",
                    "id": product.id,
                    "title": product.name,
                    "subtitle": f"{product.category} • {product.seller}",
                    "value": f"{product.price} ብር",
                    "extra": f"Stock: {product.stock}",
                    "data": {
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "stock": product.stock,
                        "category": product.category,
                        "seller": product.seller,
                        "rating": product.rating
                    }
                })
        
        # Search orders
        for order in orders:
            if (query_lower in order.product.lower() or 
                query_lower in order.status.lower() or 
                query_lower in order.id.lower() or
                query_lower in str(order.amount) or
                query_lower in order.date):
                results.append({
                    "type": "order",
                    "id": order.id,
                    "title": order.product,
                    "subtitle": f"Order {order.id} • {order.date}",
                    "value": f"{order.amount} ብር",
                    "extra": order.status,
                    "data": {
                        "id": order.id,
                        "product": order.product,
                        "amount": order.amount,
                        "status": order.status,
                        "date": order.date
                    }
                })
        
        # Search analytics terms
        analytics_terms = {
            "revenue": {"title": "Total Revenue", "value": "View Revenue Analytics", "action": "revenue"},
            "ገቢ": {"title": "Total Revenue", "value": "View Revenue Analytics", "action": "revenue"},
            "orders": {"title": "Active Orders", "value": "View Orders", "action": "orders"},
            "ትዕዛዝ": {"title": "Active Orders", "value": "View Orders", "action": "orders"},
            "inventory": {"title": "Inventory Management", "value": "View Inventory", "action": "inventory"},
            "ክምችት": {"title": "Inventory Management", "value": "View Inventory", "action": "inventory"},
            "alerts": {"title": "System Alerts", "value": "View Alerts", "action": "alerts"},
            "ማስጠንቀቂያ": {"title": "System Alerts", "value": "View Alerts", "action": "alerts"}
        }
        
        for term, data in analytics_terms.items():
            if term in query_lower:
                results.append({
                    "type": "analytics",
                    "id": data["action"],
                    "title": data["title"],
                    "subtitle": "Dashboard Analytics",
                    "value": data["value"],
                    "extra": "Click to navigate",
                    "data": {"action": data["action"]}
                })
        
        return {
            "results": results[:20],  # Limit to 20 results
            "total": len(results),
            "query": q
        }
        
    except Exception as e:
        print(f"Search error: {e}")
        return {"results": [], "total": 0, "query": q, "error": str(e)}

@app.post("/ask")
async def sql_query(query: Query, current_user: dict = Depends(get_current_user)):
    """Structured data endpoint (Inventory/Orders)."""
    try:
        generated_sql = sql_agent.query_inventory(query.prompt)
        with db_engine.connect() as connection:
            result_proxy = connection.execute(text(generated_sql))
            # Convert result to string or list for summarizer
            if result_proxy.returns_rows:
                rows = [dict(row._mapping) for row in result_proxy]
                result_str = json.dumps(rows, indent=2)
            else:
                result_str = "Operation completed successfully."
        
        # Summarize for a human response
        answer = sql_agent.summarize_results(result_str, query.prompt)
        return {
            "agent": "sql",
            "answer": answer,
            "sources": ["Marketplace SQL Database"],
            "confidence": 1.0
        }
    except Exception as e:
        error_message = str(e).lower()
        
        if "resource_exhausted" in error_message or "quota" in error_message or "429" in error_message:
            return {
                "agent": "sql",
                "answer": "SQL Agent experienced a technical hurdle. Our AI service is temporarily at capacity. Please try again in a few moments.",
                "sources": [],
                "confidence": 0.0
            }
        else:
            return {
                "agent": "sql",
                "answer": "SQL Agent experienced a technical hurdle. Please try again or contact support if the issue persists.",
                "sources": [],
                "confidence": 0.0
            }

@app.post("/rag/ask")
async def rag_query(query: Query, current_user: dict = Depends(get_current_user)):
    """Unstructured data endpoint (Documents/PDFs)."""
    if not rag_agent:
        return {
            "agent": "rag",
            "answer": "The Knowledge Base is currently unavailable. Please try again later.",
            "sources": [],
            "confidence": 0.0
        }
    
    try:
        # Agent.ask now returns a dict with the correct schema
        result = rag_agent.ask(query.prompt)
        result["agent"] = "rag"
        return result
    except Exception as e:
        return {
            "agent": "rag",
            "answer": f"I had trouble reading the documents. Error: {str(e)}",
            "sources": [],
            "confidence": 0.0
        }

# Removed duplicate import and comments

@app.post("/rag/upload")
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    """Uploads a file and automatically triggers background indexing."""
    file_path = os.path.join(DATA_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Trigger background sync
        if rag_agent:
            # We use force=True to bypass the DISABLE_RAG_SYNC env var for explicit user uploads
            background_tasks.add_task(rag_agent.sync_local_documents, DATA_DIR, force=True)
            
        return {"filename": file.filename, "status": "Uploaded. Indexing started in background."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/rag/documents")
async def list_documents(current_user: dict = Depends(get_current_user)):
    """Lists all uploaded documents."""
    files = []
    for filename in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, filename)
        if os.path.isfile(path):
            stats = os.stat(path)
            content = ""
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read(500) # Snippet for UI
            except:
                content = "[Binary or unreadable content]"
                
            files.append({
                "id": filename,
                "name": filename,
                "size": f"{(stats.st_size / 1024):.1f} KB",
                "type": filename.split('.')[-1].upper(),
                "content": content,
                "uploadedAt": stats.st_mtime * 1000 # Convert to ms for JS Date
            })
    return files

@app.delete("/rag/documents/{filename}")
async def delete_document(filename: str):
    """Deletes a document from disk."""
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Ensure agent is initialized to handle vector store deletion
        if rag_agent:
            # Also remove from vector store
            rag_agent.delete_document(filename)
            
        os.remove(file_path)
        # We do NOT trigger sync on delete automatically.
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")

@app.post("/seller/ask")
async def seller_advice(query: Query, current_user: dict = Depends(get_current_user)):
    """Strategic advice endpoint for sellers."""
    if not seller_agent:
        return {
            "agent": "seller",
            "answer": "Seller Consultant is currently offline.",
            "sources": [],
            "confidence": 0.0
        }
    
    try:
        context = get_market_snapshot()
        # get_advice now returns a dict {answer, notification}
        result = seller_agent.get_advice(query.prompt, data_context=context)
        
        response = {
            "agent": "seller",
            "answer": result["answer"],
            "sources": ["Market Intelligence Engine"],
            "confidence": 0.8
        }
        
        if result.get("notification"):
            response["notifications"] = [result["notification"]]
            
        return response
    except Exception as e:
        return {
            "agent": "seller",
            "answer": f"Consultant error: {str(e)}",
            "sources": [],
            "confidence": 0.0
        }

@app.post("/ops/ask")
async def ops_management(query: Query, current_user: dict = Depends(get_current_user)):
    """Logistics and operations management endpoint."""
    if not ops_agent:
        return {
            "agent": "ops",
            "answer": "Operations manager is unavailable.",
            "sources": [],
            "confidence": 0.0
        }
    try:
        # manage_ops now returns a dict {answer, notification}
        result = ops_agent.manage_ops(query.prompt)
        
        response = {
            "agent": "ops",
            "answer": result["answer"],
            "sources": ["Logistics Management System"],
            "confidence": 1.0
        }
        
        if result.get("notification"):
            response["notifications"] = [result["notification"]]
            
        return response
    except Exception as e:
        return {
            "agent": "ops",
            "answer": f"Ops error: {str(e)}",
            "sources": [],
            "confidence": 0.0
        }

@app.post("/recommendation/ask")
async def recommendation_query(query: Query, current_user: dict = Depends(get_current_user)):
    """Recommendation engine endpoint for pricing, inventory, and demand insights."""
    if not recommendation_agent:
        return {
            "agent": "recommendation",
            "answer": "Recommendation engine is currently unavailable.",
            "sources": [],
            "confidence": 0.0
        }
    try:
        # Extract seller_id from user_id if available
        seller_id = query.user_id if query.user_id != "system" else None
        
        # Generate recommendations
        result = recommendation_agent.generate_recommendations(
            query=query.prompt,
            seller_id=seller_id
        )
        
        # Format response for frontend
        response = {
            "agent": "recommendation",
            "answer": result.get("summary", "Generated recommendations successfully."),
            "sources": ["Recommendation Engine", "Marketplace Analytics"],
            "confidence": 0.9,
            "recommendations": result.get("recommendations", []),
            "recommendation_type": result.get("recommendation_type", "GENERAL"),
            "ethiopian_context": result.get("ethiopian_context", "")
        }
        
        return response
    except Exception as e:
        error_message = str(e).lower()
        
        if "resource_exhausted" in error_message or "quota" in error_message or "429" in error_message:
            return {
                "agent": "recommendation",
                "answer": "Recommendation Agent experienced a technical hurdle. Our AI service is temporarily at capacity. Please try again in a few moments.",
                "sources": [],
                "confidence": 0.0
            }
        else:
            return {
                "agent": "recommendation",
                "answer": "Recommendation Agent experienced a technical hurdle. Please try again or contact support if the issue persists.",
                "sources": [],
                "confidence": 0.0
            }

@app.post("/workflow/ask")
async def unified_query(query: Query, current_user: dict = Depends(get_current_user)):
    """Intelligent routing endpoint using WorkflowAgent."""
    if not workflow_agent:
        return {
            "agent": "workflow",
            "answer": "The system is currently undergoing maintenance. Please try again soon.",
            "sources": [],
            "confidence": 0.0
        }
    
    target = workflow_agent.route_query(query.prompt)
    
    if target == "sql":
        return await sql_query(query)
    elif target == "rag":
        return await rag_query(query)
    elif target == "recommendation":
        return await recommendation_query(query)
    elif target == "seller":
        return await seller_advice(query)
    elif target == "fraud":
        return await fraud_detection_query(query)
    else:
        return await ops_management(query)

# --- Fraud Detection Endpoints ---

class FraudScanRequest(BaseModel):
    scan_type: Optional[str] = "full"  # full, pricing, transactions, inventory, coordinated

class AlertStatusUpdate(BaseModel):
    status: str  # active, investigating, resolved, false_positive
    resolved_by: Optional[str] = None
    notes: Optional[str] = None

class TransactionCheck(BaseModel):
    transaction_id: str
    user_id: str
    product: str
    amount: float
    timestamp: Optional[str] = None

class ContactFormData(BaseModel):
    name: str
    email: str
    company: Optional[str] = None
    subject: str
    message: str
    projectType: str

@app.post("/fraud/scan")
async def run_fraud_scan(request: FraudScanRequest, current_user: dict = Depends(get_current_user)):
    """Run fraud detection scan on marketplace data."""
    if not fraud_detection_service:
        return {
            "status": "error",
            "message": "Fraud detection service is not available",
            "alerts": []
        }
    
    try:
        result = fraud_detection_service.run_fraud_scan(
            scan_type=request.scan_type,
            save_results=True
        )
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Fraud scan failed: {str(e)}",
            "alerts": []
        }

@app.get("/fraud/alerts")
async def get_fraud_alerts(risk_level: Optional[str] = None, limit: int = 50):
    """Get active fraud alerts."""
    if not fraud_detection_service:
        return {"alerts": [], "message": "Fraud detection service not available"}
    
    try:
        alerts = fraud_detection_service.get_active_alerts(
            risk_level=risk_level,
            limit=limit
        )
        return {"alerts": alerts, "total": len(alerts)}
    except Exception as e:
        return {"alerts": [], "error": str(e)}

@app.get("/fraud/alerts/{alert_id}")
async def get_alert_details(alert_id: str):
    """Get detailed information about a specific fraud alert."""
    if not fraud_detection_service:
        raise HTTPException(status_code=503, detail="Fraud detection service not available")
    
    try:
        alert = fraud_detection_service.get_alert_details(alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return alert
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/fraud/alerts/{alert_id}/status")
async def update_alert_status(alert_id: str, update: AlertStatusUpdate):
    """Update the status of a fraud alert."""
    if not fraud_detection_service:
        raise HTTPException(status_code=503, detail="Fraud detection service not available")
    
    try:
        success = fraud_detection_service.update_alert_status(
            alert_id=alert_id,
            status=update.status,
            resolved_by=update.resolved_by,
            notes=update.notes
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return {"status": "success", "message": "Alert status updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/fraud/statistics")
async def get_fraud_statistics(days: int = 30):
    """Get fraud detection statistics for the specified period."""
    if not fraud_detection_service:
        return {
            "error": "Fraud detection service not available",
            "statistics": {}
        }
    
    try:
        stats = fraud_detection_service.get_fraud_statistics(days=days)
        return {"statistics": stats}
    except Exception as e:
        return {"error": str(e), "statistics": {}}

@app.post("/api/contact")
async def contact_form_submission(contact_data: ContactFormData):
    """Handle contact form submissions and send email to jossyyasub@gmail.com."""
    try:
        # Validate required fields
        if not contact_data.name.strip():
            raise HTTPException(status_code=400, detail="Name is required")
        if not contact_data.email.strip():
            raise HTTPException(status_code=400, detail="Email is required")
        if not contact_data.subject.strip():
            raise HTTPException(status_code=400, detail="Subject is required")
        if not contact_data.message.strip():
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Format email content
        project_types = {
            'consultation': 'Technical Consultation',
            'ai-development': 'AI System Development',
            'backend-development': 'Backend Development',
            'fullstack-project': 'Full-Stack Project',
            'database-design': 'Database Architecture',
            'system-integration': 'System Integration',
            'other': 'Other Services'
        }
        
        project_type_label = project_types.get(contact_data.projectType, contact_data.projectType)
        
        email_subject = f"New Contact Form: {contact_data.subject}"
        
        email_body = f"""
New contact form submission from your portfolio website:

Name: {contact_data.name}
Email: {contact_data.email}
Company: {contact_data.company or 'Not provided'}
Project Type: {project_type_label}
Subject: {contact_data.subject}

Message:
{contact_data.message}

---
This message was sent from your portfolio contact form.
Reply directly to {contact_data.email} to respond to the inquiry.
        """.strip()
        
        # Send email using EmailService
        email_result = EmailService.send_email(
            to="jossyyasub@gmail.com",
            subject=email_subject,
            body=email_body
        )
        
        # Log the contact form submission
        print(f"Contact form submission from {contact_data.name} ({contact_data.email})")
        print(f"Project Type: {project_type_label}")
        print(f"Subject: {contact_data.subject}")
        
        return {
            "status": "success",
            "message": "Your message has been sent successfully! I'll get back to you within 24 hours.",
            "email_status": email_result.get("details", {}).get("status", "sent")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Contact form error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to send message. Please try again or contact me directly at jossyyasub@gmail.com"
        )

@app.post("/fraud/check-transaction")
async def check_transaction(transaction: TransactionCheck):
    """Perform real-time fraud check on a transaction."""
    if not fraud_detection_service:
        return {
            "transaction_id": transaction.transaction_id,
            "risk_score": 0,
            "risk_level": "unknown",
            "approved": True,
            "error": "Fraud detection service not available"
        }
    
    try:
        result = fraud_detection_service.check_real_time_transaction({
            "id": transaction.transaction_id,
            "user_id": transaction.user_id,
            "product": transaction.product,
            "amount": transaction.amount,
            "timestamp": transaction.timestamp
        })
        return result
    except Exception as e:
        return {
            "transaction_id": transaction.transaction_id,
            "risk_score": 0,
            "risk_level": "error",
            "approved": False,
            "error": str(e)
        }

@app.post("/fraud/create-user-profile/{user_id}")
async def create_user_profile(user_id: str):
    """Create or update user behavior profile for fraud detection."""
    if not fraud_detection_service:
        raise HTTPException(status_code=503, detail="Fraud detection service not available")
    
    try:
        success = fraud_detection_service.create_user_behavior_profile(user_id)
        if success:
            return {"status": "success", "message": f"User profile created/updated for {user_id}"}
        else:
            return {"status": "warning", "message": f"No transaction data found for user {user_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/fraud/ask")
async def fraud_detection_query(query: Query):
    """Natural language interface for fraud detection queries."""
    if not fraud_detection_service:
        return {
            "agent": "fraud_detection",
            "answer": "Fraud detection system is currently unavailable.",
            "sources": [],
            "confidence": 0.0
        }
    
    try:
        # Determine query type and route appropriately
        prompt_lower = query.prompt.lower()
        
        if any(word in prompt_lower for word in ["scan", "check", "detect", "analyze"]):
            # Run fraud scan
            result = fraud_detection_service.run_fraud_scan("full", save_results=True)
            
            if result.get("status") == "success":
                alerts_count = result.get("alerts_found", 0)
                critical_count = result.get("critical_alerts", 0)
                
                if alerts_count == 0:
                    answer = "I completed a comprehensive fraud scan and found no suspicious activities. All marketplace transactions and patterns appear normal."
                else:
                    answer = f"I detected {alerts_count} potential fraud indicators, including {critical_count} critical alerts that need immediate attention. {result.get('summary', '')}"
                
                return {
                    "agent": "fraud_detection",
                    "answer": answer,
                    "sources": ["Fraud Detection Engine", "Transaction Analysis"],
                    "confidence": 0.9,
                    "scan_results": result
                }
            else:
                return {
                    "agent": "fraud_detection",
                    "answer": f"I encountered an issue while scanning for fraud: {result.get('message', 'Unknown error')}",
                    "sources": [],
                    "confidence": 0.0
                }
        
        elif any(word in prompt_lower for word in ["alert", "investigation", "details"]):
            # Get alert information
            alerts = fraud_detection_service.get_active_alerts(limit=10)
            
            if not alerts:
                answer = "There are currently no active fraud alerts. The marketplace appears secure."
            else:
                high_risk = len([a for a in alerts if a["risk_level"] in ["critical", "high"]])
                answer = f"I found {len(alerts)} active fraud alerts, with {high_risk} requiring immediate attention. The most serious issues involve {', '.join(set(a['type'].replace('_', ' ') for a in alerts[:3]))}."
            
            return {
                "agent": "fraud_detection",
                "answer": answer,
                "sources": ["Fraud Alert Database"],
                "confidence": 0.9,
                "alerts": alerts[:5]  # Return top 5 alerts
            }
        
        elif any(word in prompt_lower for word in ["statistics", "stats", "report", "summary"]):
            # Get fraud statistics
            stats = fraud_detection_service.get_fraud_statistics(days=30)
            
            total_alerts = stats.get("total_alerts", 0)
            accuracy = stats.get("accuracy_rate", 0)
            
            if total_alerts == 0:
                answer = "Over the past 30 days, no fraud has been detected. The marketplace has maintained excellent security with no suspicious activities reported."
            else:
                answer = f"In the past 30 days, I detected {total_alerts} potential fraud cases with {accuracy:.1f}% accuracy. The most common fraud types are {', '.join(stats.get('fraud_types', {}).keys())}."
            
            return {
                "agent": "fraud_detection",
                "answer": answer,
                "sources": ["Fraud Statistics Database"],
                "confidence": 0.9,
                "statistics": stats
            }
        
        else:
            # General fraud detection information
            return {
                "agent": "fraud_detection",
                "answer": "I'm your fraud detection specialist. I can scan for suspicious activities, investigate alerts, provide fraud statistics, and help protect the marketplace. What would you like me to check?",
                "sources": ["Fraud Detection System"],
                "confidence": 1.0
            }
    
    except Exception as e:
        return {
            "agent": "fraud_detection",
            "answer": f"I encountered an error while processing your fraud detection request: {str(e)}",
            "sources": [],
            "confidence": 0.0
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)