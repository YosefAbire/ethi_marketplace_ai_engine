"""
Database schema for fraud detection system.
This module defines the tables needed for fraud detection and monitoring.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class FraudAlert(Base):
    """
    Stores fraud detection alerts and their details.
    """
    __tablename__ = "fraud_alerts"
    
    id = Column(String, primary_key=True, index=True)
    fraud_type = Column(String, nullable=False)  # pricing_manipulation, account_fraud, etc.
    risk_level = Column(String, nullable=False)  # low, medium, high, critical
    risk_score = Column(Float, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    evidence = Column(JSON)  # Store evidence as JSON
    affected_entities = Column(JSON)  # List of affected user_ids, product_ids, etc.
    recommended_actions = Column(JSON)  # List of recommended actions
    confidence = Column(Float, nullable=False)
    status = Column(String, default="active")  # active, investigating, resolved, false_positive
    ethiopian_context = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime)
    resolved_by = Column(String)  # User who resolved the alert
    resolution_notes = Column(Text)

class UserBehaviorProfile(Base):
    """
    Stores user behavior profiles for anomaly detection.
    """
    __tablename__ = "user_behavior_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, unique=True, index=True)
    avg_transaction_amount = Column(Float, default=0.0)
    avg_session_duration = Column(Float, default=0.0)  # in minutes
    typical_login_hours = Column(JSON)  # List of typical login hours
    common_products = Column(JSON)  # List of commonly purchased products
    transaction_frequency = Column(Float, default=0.0)  # transactions per day
    login_frequency = Column(Float, default=0.0)  # logins per day
    avg_cart_size = Column(Float, default=0.0)
    preferred_categories = Column(JSON)  # List of preferred product categories
    risk_score = Column(Float, default=0.0)  # Overall user risk score
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class PricingHistory(Base):
    """
    Tracks pricing changes for fraud detection analysis.
    """
    __tablename__ = "pricing_history"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    product_name = Column(String, nullable=False)
    old_price = Column(Float, nullable=False)
    new_price = Column(Float, nullable=False)
    price_change_percentage = Column(Float, nullable=False)
    seller = Column(String, nullable=False)
    category = Column(String, nullable=False)
    change_reason = Column(String)  # seasonal, promotion, market_adjustment, etc.
    is_flagged = Column(Boolean, default=False)
    changed_at = Column(DateTime, default=datetime.utcnow)

class TransactionPattern(Base):
    """
    Stores transaction patterns for fraud detection.
    """
    __tablename__ = "transaction_patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    pattern_type = Column(String, nullable=False)  # wash_trading, volume_spike, etc.
    product_name = Column(String, nullable=False)
    seller = Column(String, nullable=False)
    pattern_data = Column(JSON)  # Detailed pattern information
    risk_score = Column(Float, nullable=False)
    detection_date = Column(DateTime, default=datetime.utcnow)
    is_confirmed = Column(Boolean, default=False)
    notes = Column(Text)

class InventoryAudit(Base):
    """
    Tracks inventory changes for fraud detection.
    """
    __tablename__ = "inventory_audits"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    product_name = Column(String, nullable=False)
    seller = Column(String, nullable=False)
    old_stock = Column(Integer, nullable=False)
    new_stock = Column(Integer, nullable=False)
    stock_change = Column(Integer, nullable=False)
    change_type = Column(String, nullable=False)  # restock, sale, adjustment, suspicious
    is_suspicious = Column(Boolean, default=False)
    audit_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

class FraudInvestigation(Base):
    """
    Tracks fraud investigations and their outcomes.
    """
    __tablename__ = "fraud_investigations"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String, ForeignKey('fraud_alerts.id'), nullable=False)
    investigator = Column(String, nullable=False)
    investigation_status = Column(String, default="open")  # open, in_progress, closed
    findings = Column(Text)
    evidence_collected = Column(JSON)
    actions_taken = Column(JSON)
    outcome = Column(String)  # confirmed_fraud, false_positive, inconclusive
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationship
    alert = relationship("FraudAlert", backref="investigations")

class FraudStatistics(Base):
    """
    Stores fraud detection statistics for reporting and analysis.
    """
    __tablename__ = "fraud_statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, index=True)
    total_alerts = Column(Integer, default=0)
    critical_alerts = Column(Integer, default=0)
    high_risk_alerts = Column(Integer, default=0)
    medium_risk_alerts = Column(Integer, default=0)
    low_risk_alerts = Column(Integer, default=0)
    false_positives = Column(Integer, default=0)
    confirmed_fraud = Column(Integer, default=0)
    avg_detection_time = Column(Float, default=0.0)  # in minutes
    avg_resolution_time = Column(Float, default=0.0)  # in minutes
    fraud_types_detected = Column(JSON)  # Count by fraud type
    created_at = Column(DateTime, default=datetime.utcnow)

class WhitelistedEntity(Base):
    """
    Stores whitelisted entities that should be excluded from certain fraud checks.
    """
    __tablename__ = "whitelisted_entities"
    
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, nullable=False)  # user, product, seller
    entity_id = Column(String, nullable=False)
    entity_name = Column(String, nullable=False)
    whitelist_reason = Column(String, nullable=False)
    exempted_checks = Column(JSON)  # List of fraud checks to skip
    added_by = Column(String, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)  # Optional expiration
    is_active = Column(Boolean, default=True)
    notes = Column(Text)

class FraudRule(Base):
    """
    Stores configurable fraud detection rules and thresholds.
    """
    __tablename__ = "fraud_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String, nullable=False, unique=True)
    rule_type = Column(String, nullable=False)  # pricing, transaction, inventory, etc.
    description = Column(Text, nullable=False)
    conditions = Column(JSON, nullable=False)  # Rule conditions as JSON
    threshold_value = Column(Float, nullable=False)
    risk_score_impact = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    severity = Column(String, default="medium")  # low, medium, high, critical
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_triggered = Column(DateTime)

def create_fraud_tables(engine):
    """
    Create all fraud detection tables in the database.
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Created fraud detection tables successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating fraud detection tables: {e}")
        return False

def get_table_info():
    """
    Return information about fraud detection tables for documentation.
    """
    return {
        "fraud_alerts": "Main table for storing fraud detection alerts",
        "user_behavior_profiles": "User behavior patterns for anomaly detection",
        "pricing_history": "Historical pricing data for trend analysis",
        "transaction_patterns": "Detected transaction patterns and anomalies",
        "inventory_audits": "Inventory change tracking for fraud detection",
        "fraud_investigations": "Investigation records and outcomes",
        "fraud_statistics": "Daily fraud detection statistics",
        "whitelisted_entities": "Entities exempt from certain fraud checks",
        "fraud_rules": "Configurable fraud detection rules and thresholds"
    }