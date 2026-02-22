#!/usr/bin/env python3
"""
Setup script for fraud detection system.
This script will:
1. Create fraud detection tables in the database
2. Initialize sample fraud rules
3. Set up user behavior profiles for existing users
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import json

# Load environment variables
load_dotenv()

# Import fraud detection schema
from fraud_detection_schema import (
    create_fraud_tables, 
    FraudRule, 
    UserBehaviorProfile,
    WhitelistedEntity
)

def setup_fraud_detection():
    """Set up fraud detection system in the database."""
    print("=== Fraud Detection System Setup ===\n")
    
    # Get database connection
    database_url = os.getenv("DATABASE_URL", "sqlite:///./marketplace.db")
    engine = create_engine(database_url)
    
    print(f"Connecting to database: {database_url.split('://')[0]}")
    
    # Step 1: Create fraud detection tables
    print("\nStep 1: Creating fraud detection tables...")
    if create_fraud_tables(engine):
        print("✓ Fraud detection tables created successfully")
    else:
        print("✗ Failed to create fraud detection tables")
        return False
    
    # Step 2: Initialize fraud rules
    print("\nStep 2: Setting up fraud detection rules...")
    if setup_fraud_rules(engine):
        print("✓ Fraud detection rules configured")
    else:
        print("✗ Failed to configure fraud rules")
    
    # Step 3: Create user behavior profiles for existing users
    print("\nStep 3: Initializing user behavior profiles...")
    if initialize_user_profiles(engine):
        print("✓ User behavior profiles initialized")
    else:
        print("✗ Failed to initialize user profiles")
    
    # Step 4: Set up whitelisted entities
    print("\nStep 4: Configuring whitelisted entities...")
    if setup_whitelisted_entities(engine):
        print("✓ Whitelisted entities configured")
    else:
        print("✗ Failed to configure whitelisted entities")
    
    print("\n🎉 Fraud Detection System setup completed!")
    print("\nNext steps:")
    print("1. Restart your application to load the fraud detection service")
    print("2. Access fraud detection via /fraud/scan endpoint")
    print("3. Monitor alerts via /fraud/alerts endpoint")
    print("4. Configure additional rules as needed")
    
    return True

def setup_fraud_rules(engine):
    """Initialize default fraud detection rules."""
    try:
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        # Check if rules already exist
        existing_rules = db.query(FraudRule).count()
        if existing_rules > 0:
            print(f"  Found {existing_rules} existing fraud rules, skipping initialization")
            db.close()
            return True
        
        # Default fraud detection rules
        default_rules = [
            {
                "rule_name": "price_spike_detection",
                "rule_type": "pricing",
                "description": "Detect abnormal price increases beyond seasonal patterns",
                "conditions": {
                    "price_increase_threshold": 0.5,
                    "exclude_seasonal": True,
                    "minimum_price": 1.0
                },
                "threshold_value": 50.0,
                "risk_score_impact": 30.0,
                "severity": "high",
                "created_by": "system"
            },
            {
                "rule_name": "wash_trading_detection",
                "rule_type": "transaction",
                "description": "Detect repeated identical transactions indicating wash trading",
                "conditions": {
                    "identical_amount_threshold": 0.3,
                    "minimum_transactions": 10,
                    "time_window_hours": 24
                },
                "threshold_value": 30.0,
                "risk_score_impact": 40.0,
                "severity": "critical",
                "created_by": "system"
            },
            {
                "rule_name": "phantom_inventory_detection",
                "rule_type": "inventory",
                "description": "Detect high stock levels with no recent sales",
                "conditions": {
                    "high_stock_threshold": 100,
                    "no_sales_days": 7,
                    "exclude_seasonal_products": True
                },
                "threshold_value": 70.0,
                "risk_score_impact": 25.0,
                "severity": "medium",
                "created_by": "system"
            },
            {
                "rule_name": "coordinated_pricing_detection",
                "rule_type": "pricing",
                "description": "Detect coordinated pricing across multiple sellers",
                "conditions": {
                    "identical_pricing_threshold": 1.0,
                    "minimum_sellers": 3,
                    "same_category": True
                },
                "threshold_value": 80.0,
                "risk_score_impact": 35.0,
                "severity": "high",
                "created_by": "system"
            },
            {
                "rule_name": "transaction_volume_spike",
                "rule_type": "transaction",
                "description": "Detect unusual spikes in transaction volume",
                "conditions": {
                    "volume_multiplier": 5.0,
                    "baseline_period_days": 30,
                    "minimum_baseline_transactions": 5
                },
                "threshold_value": 60.0,
                "risk_score_impact": 20.0,
                "severity": "medium",
                "created_by": "system"
            }
        ]
        
        # Add rules to database
        for rule_data in default_rules:
            rule = FraudRule(**rule_data)
            db.add(rule)
        
        db.commit()
        db.close()
        
        print(f"  Added {len(default_rules)} default fraud detection rules")
        return True
        
    except Exception as e:
        print(f"  Error setting up fraud rules: {e}")
        return False

def initialize_user_profiles(engine):
    """Create user behavior profiles for existing users."""
    try:
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        # Check if profiles already exist
        existing_profiles = db.query(UserBehaviorProfile).count()
        if existing_profiles > 0:
            print(f"  Found {existing_profiles} existing user profiles, skipping initialization")
            db.close()
            return True
        
        # Get existing users from orders (simplified approach)
        with engine.connect() as conn:
            # Extract unique user patterns from order IDs
            orders_query = text("SELECT DISTINCT id FROM orders LIMIT 10")
            result = conn.execute(orders_query)
            orders = [row[0] for row in result]
        
        if not orders:
            print("  No existing orders found, skipping user profile creation")
            return True
        
        # Create sample user profiles based on order patterns
        sample_profiles = []
        for i, order_id in enumerate(orders[:5]):  # Create profiles for first 5 users
            user_id = f"user_{i+1}"
            profile = UserBehaviorProfile(
                user_id=user_id,
                avg_transaction_amount=50.0 + (i * 20),  # Varied amounts
                avg_session_duration=15.0 + (i * 5),     # 15-35 minutes
                typical_login_hours=[9, 10, 14, 15, 16], # Business hours
                common_products=["teff", "honey", "coffee"][:i+1],
                transaction_frequency=2.0 + (i * 0.5),   # 2-4 transactions per day
                login_frequency=1.0 + (i * 0.2),         # 1-2 logins per day
                avg_cart_size=2.0 + (i * 0.5),           # 2-4 items per cart
                preferred_categories=["Grains", "Natural Foods", "Coffee"][:i+1],
                risk_score=10.0 + (i * 5),               # Low risk scores
                last_updated=datetime.utcnow()
            )
            sample_profiles.append(profile)
        
        # Add profiles to database
        for profile in sample_profiles:
            db.add(profile)
        
        db.commit()
        db.close()
        
        print(f"  Created {len(sample_profiles)} sample user behavior profiles")
        return True
        
    except Exception as e:
        print(f"  Error initializing user profiles: {e}")
        return False

def setup_whitelisted_entities(engine):
    """Set up whitelisted entities that should be excluded from certain fraud checks."""
    try:
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        # Check if whitelist entries already exist
        existing_entries = db.query(WhitelistedEntity).count()
        if existing_entries > 0:
            print(f"  Found {existing_entries} existing whitelist entries, skipping initialization")
            db.close()
            return True
        
        # Default whitelisted entities
        whitelist_entries = [
            {
                "entity_type": "seller",
                "entity_id": "Adane Farms",
                "entity_name": "Adane Farms - Premium Teff Producer",
                "whitelist_reason": "Verified premium seller with seasonal pricing patterns",
                "exempted_checks": ["price_spike_detection"],
                "added_by": "system",
                "expires_at": datetime.utcnow() + timedelta(days=365),
                "notes": "Legitimate seasonal price variations for agricultural products"
            },
            {
                "entity_type": "product",
                "entity_id": "teff",
                "entity_name": "Teff Products",
                "whitelist_reason": "Traditional Ethiopian grain with known seasonal patterns",
                "exempted_checks": ["price_spike_detection", "phantom_inventory_detection"],
                "added_by": "system",
                "expires_at": datetime.utcnow() + timedelta(days=365),
                "notes": "Seasonal harvest patterns cause natural price and inventory fluctuations"
            },
            {
                "entity_type": "user",
                "entity_id": "system",
                "entity_name": "System Administrator",
                "whitelist_reason": "Administrative account for system operations",
                "exempted_checks": ["transaction_volume_spike", "wash_trading_detection"],
                "added_by": "system",
                "notes": "System account for testing and administrative operations"
            }
        ]
        
        # Add whitelist entries to database
        for entry_data in whitelist_entries:
            entry = WhitelistedEntity(**entry_data)
            db.add(entry)
        
        db.commit()
        db.close()
        
        print(f"  Added {len(whitelist_entries)} whitelist entries")
        return True
        
    except Exception as e:
        print(f"  Error setting up whitelisted entities: {e}")
        return False

def test_fraud_detection_setup(engine):
    """Test the fraud detection setup."""
    try:
        print("\nTesting fraud detection setup...")
        
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        # Test table creation
        rules_count = db.query(FraudRule).count()
        profiles_count = db.query(UserBehaviorProfile).count()
        whitelist_count = db.query(WhitelistedEntity).count()
        
        print(f"✓ Fraud rules: {rules_count}")
        print(f"✓ User profiles: {profiles_count}")
        print(f"✓ Whitelist entries: {whitelist_count}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = setup_fraud_detection()
    
    if success:
        # Test the setup
        database_url = os.getenv("DATABASE_URL", "sqlite:///./marketplace.db")
        engine = create_engine(database_url)
        test_fraud_detection_setup(engine)
        
        print("\n" + "="*50)
        print("Fraud Detection System is ready!")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("Setup failed. Please check the errors above.")
        print("="*50)
        sys.exit(1)