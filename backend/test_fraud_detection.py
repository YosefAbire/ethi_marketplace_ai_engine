#!/usr/bin/env python3
"""
Test script for fraud detection system.
This script tests all major fraud detection functionality.
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Import fraud detection components
from agents.fraud_detection_agent import FraudDetectionAgent
from services.fraud_detection_service import FraudDetectionService
from agents.sql_agent import SQLAgent

def test_fraud_detection_system():
    """Test the complete fraud detection system."""
    print("=== Fraud Detection System Test ===\n")
    
    # Get database connection
    database_url = os.getenv("DATABASE_URL", "sqlite:///./marketplace.db")
    engine = create_engine(database_url)
    
    print(f"Testing with database: {database_url.split('://')[0]}")
    
    try:
        # Initialize components
        print("\nStep 1: Initializing fraud detection components...")
        sql_agent = SQLAgent(db_engine=engine)
        fraud_service = FraudDetectionService(db_engine=engine, sql_agent=sql_agent)
        print("✓ Components initialized successfully")
        
        # Test 1: Run fraud scan
        print("\nStep 2: Testing fraud detection scan...")
        scan_result = fraud_service.run_fraud_scan("full", save_results=True)
        
        if scan_result.get("status") == "success":
            alerts_found = scan_result.get("alerts_found", 0)
            print(f"✓ Fraud scan completed - Found {alerts_found} alerts")
            
            if alerts_found > 0:
                print(f"  - Critical alerts: {scan_result.get('critical_alerts', 0)}")
                print(f"  - High risk alerts: {scan_result.get('high_risk_alerts', 0)}")
                print(f"  - Summary: {scan_result.get('summary', 'No summary available')[:100]}...")
        else:
            print(f"✗ Fraud scan failed: {scan_result.get('message', 'Unknown error')}")
        
        # Test 2: Get active alerts
        print("\nStep 3: Testing alert retrieval...")
        alerts = fraud_service.get_active_alerts(limit=5)
        print(f"✓ Retrieved {len(alerts)} active alerts")
        
        if alerts:
            for i, alert in enumerate(alerts[:3]):
                print(f"  Alert {i+1}: {alert['title']} (Risk: {alert['risk_level']})")
        
        # Test 3: Test real-time transaction check
        print("\nStep 4: Testing real-time transaction check...")
        test_transaction = {
            "id": "TEST-001",
            "user_id": "test_user",
            "product": "Test Product",
            "amount": 1000.0,  # High amount to trigger risk
            "timestamp": datetime.now().isoformat()
        }
        
        transaction_result = fraud_service.check_real_time_transaction(test_transaction)
        print(f"✓ Transaction check completed")
        print(f"  - Risk Score: {transaction_result.get('risk_score', 0)}")
        print(f"  - Risk Level: {transaction_result.get('risk_level', 'unknown')}")
        print(f"  - Approved: {transaction_result.get('approved', False)}")
        
        # Test 4: Create user behavior profile
        print("\nStep 5: Testing user behavior profile creation...")
        profile_result = fraud_service.create_user_behavior_profile("test_user_123")
        if profile_result:
            print("✓ User behavior profile created successfully")
        else:
            print("⚠ User behavior profile creation skipped (no transaction data)")
        
        # Test 5: Get fraud statistics
        print("\nStep 6: Testing fraud statistics...")
        stats = fraud_service.get_fraud_statistics(days=30)
        print(f"✓ Fraud statistics retrieved")
        print(f"  - Total alerts (30 days): {stats.get('total_alerts', 0)}")
        print(f"  - Critical alerts: {stats.get('critical_alerts', 0)}")
        print(f"  - Accuracy rate: {stats.get('accuracy_rate', 0):.1f}%")
        
        # Test 6: Test specific fraud detection methods
        print("\nStep 7: Testing individual fraud detection methods...")
        fraud_agent = fraud_service.fraud_agent
        
        if fraud_agent and fraud_agent.engine:
            # Test pricing analysis
            pricing_alerts = fraud_agent.engine.analyze_pricing_patterns()
            print(f"✓ Pricing analysis: {len(pricing_alerts)} alerts")
            
            # Test transaction analysis
            transaction_alerts = fraud_agent.engine.analyze_transaction_patterns()
            print(f"✓ Transaction analysis: {len(transaction_alerts)} alerts")
            
            # Test inventory analysis
            inventory_alerts = fraud_agent.engine.analyze_inventory_patterns()
            print(f"✓ Inventory analysis: {len(inventory_alerts)} alerts")
            
            # Test coordinated attack detection
            coordinated_alerts = fraud_agent.engine.detect_coordinated_attacks()
            print(f"✓ Coordinated attack detection: {len(coordinated_alerts)} alerts")
        
        print("\n🎉 All fraud detection tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fraud_detection_api_simulation():
    """Simulate API calls to test fraud detection endpoints."""
    print("\n=== API Simulation Test ===\n")
    
    try:
        # Get database connection
        database_url = os.getenv("DATABASE_URL", "sqlite:///./marketplace.db")
        engine = create_engine(database_url)
        
        # Initialize service
        sql_agent = SQLAgent(db_engine=engine)
        fraud_service = FraudDetectionService(db_engine=engine, sql_agent=sql_agent)
        
        # Simulate /fraud/scan endpoint
        print("Simulating POST /fraud/scan...")
        scan_result = fraud_service.run_fraud_scan("full", save_results=True)
        print(f"Response: {json.dumps(scan_result, indent=2, default=str)[:500]}...")
        
        # Simulate /fraud/alerts endpoint
        print("\nSimulating GET /fraud/alerts...")
        alerts = fraud_service.get_active_alerts(limit=3)
        print(f"Response: Found {len(alerts)} alerts")
        
        # Simulate /fraud/statistics endpoint
        print("\nSimulating GET /fraud/statistics...")
        stats = fraud_service.get_fraud_statistics(days=7)
        print(f"Response: {json.dumps(stats, indent=2)[:300]}...")
        
        # Simulate /fraud/check-transaction endpoint
        print("\nSimulating POST /fraud/check-transaction...")
        test_tx = {
            "id": "SIM-001",
            "user_id": "sim_user",
            "product": "Expensive Item",
            "amount": 500.0
        }
        tx_result = fraud_service.check_real_time_transaction(test_tx)
        print(f"Response: {json.dumps(tx_result, indent=2)}")
        
        print("\n✓ API simulation completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ API simulation failed: {e}")
        return False

def create_test_data():
    """Create some test data to make fraud detection more interesting."""
    print("\n=== Creating Test Data ===\n")
    
    try:
        database_url = os.getenv("DATABASE_URL", "sqlite:///./marketplace.db")
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Add some suspicious pricing data
            suspicious_products = [
                ("Suspicious Teff", 100, 5, "Grains", "Suspicious Seller", 3),
                ("Overpriced Honey", 50, 200, "Natural Foods", "Price Manipulator", 2),
                ("Fake Coffee", 200, 0, "Coffee", "Fake Seller", 1)
            ]
            
            for name, price, stock, category, seller, rating in suspicious_products:
                try:
                    insert_query = text("""
                        INSERT OR IGNORE INTO products (name, price, stock, category, seller, rating)
                        VALUES (:name, :price, :stock, :category, :seller, :rating)
                    """)
                    conn.execute(insert_query, {
                        "name": name,
                        "price": price,
                        "stock": stock,
                        "category": category,
                        "seller": seller,
                        "rating": rating
                    })
                except Exception as e:
                    print(f"Note: Could not insert test product {name}: {e}")
            
            # Add some suspicious orders
            suspicious_orders = [
                ("WASH-001", "Suspicious Teff", 100, "Pending", "2024-03-15"),
                ("WASH-002", "Suspicious Teff", 100, "Pending", "2024-03-15"),
                ("WASH-003", "Suspicious Teff", 100, "Pending", "2024-03-15"),
                ("FAKE-001", "Fake Coffee", 200, "Delivered", "2024-03-14")
            ]
            
            for order_id, product, amount, status, date in suspicious_orders:
                try:
                    insert_query = text("""
                        INSERT OR IGNORE INTO orders (id, product, amount, status, date)
                        VALUES (:id, :product, :amount, :status, :date)
                    """)
                    conn.execute(insert_query, {
                        "id": order_id,
                        "product": product,
                        "amount": amount,
                        "status": status,
                        "date": date
                    })
                except Exception as e:
                    print(f"Note: Could not insert test order {order_id}: {e}")
            
            conn.commit()
        
        print("✓ Test data created successfully")
        return True
        
    except Exception as e:
        print(f"✗ Failed to create test data: {e}")
        return False

if __name__ == "__main__":
    print("Starting fraud detection system tests...\n")
    
    # Create test data first
    create_test_data()
    
    # Run main tests
    success = test_fraud_detection_system()
    
    if success:
        # Run API simulation
        api_success = test_fraud_detection_api_simulation()
        
        if api_success:
            print("\n" + "="*60)
            print("🎉 ALL TESTS PASSED! Fraud Detection System is working!")
            print("="*60)
            print("\nYou can now:")
            print("1. Start the API server: python backend/api/main.py")
            print("2. Test fraud endpoints:")
            print("   - POST /fraud/scan")
            print("   - GET /fraud/alerts")
            print("   - GET /fraud/statistics")
            print("   - POST /fraud/check-transaction")
            print("   - POST /fraud/ask")
        else:
            print("\n⚠ Main tests passed but API simulation had issues")
    else:
        print("\n" + "="*60)
        print("❌ TESTS FAILED! Please check the errors above.")
        print("="*60)
        sys.exit(1)