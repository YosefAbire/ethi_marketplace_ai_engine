"""
Fraud Detection Service
Provides high-level fraud detection operations and integrates with the main API.
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from agents.fraud_detection_agent import FraudDetectionAgent, FraudAlert, RiskLevel, FraudType
from fraud_detection_schema import (
    FraudAlert as DBFraudAlert, 
    UserBehaviorProfile, 
    PricingHistory,
    FraudStatistics,
    create_fraud_tables
)

class FraudDetectionService:
    """
    High-level service for fraud detection operations.
    Manages fraud detection agents and database operations.
    """
    
    def __init__(self, db_engine, sql_agent=None, rag_agent=None, api_key: Optional[str] = None):
        self.db_engine = db_engine
        self.api_key = api_key or os.getenv("API_KEY")
        
        # Create database session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
        self.db_session = SessionLocal()
        
        # Initialize fraud detection agent
        self.fraud_agent = FraudDetectionAgent(sql_agent, rag_agent, api_key)
        
        # Ensure fraud detection tables exist
        self._initialize_fraud_tables()
    
    def _initialize_fraud_tables(self):
        """Initialize fraud detection database tables."""
        try:
            create_fraud_tables(self.db_engine)
        except Exception as e:
            print(f"Warning: Could not create fraud detection tables: {e}")
    
    def run_fraud_scan(self, scan_type: str = "full", save_results: bool = True) -> Dict[str, Any]:
        """
        Run fraud detection scan and optionally save results to database.
        """
        try:
            # Run the fraud scan
            results = self.fraud_agent.run_fraud_scan(scan_type)
            
            if save_results and results.get("status") == "success":
                # Save alerts to database
                self._save_alerts_to_db(results.get("alerts", []))
                
                # Update fraud statistics
                self._update_fraud_statistics(results)
            
            return results
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Fraud scan failed: {str(e)}",
                "alerts": [],
                "summary": ""
            }
    
    def get_active_alerts(self, risk_level: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get active fraud alerts from database.
        """
        try:
            query = self.db_session.query(DBFraudAlert).filter(
                DBFraudAlert.status == "active"
            )
            
            if risk_level:
                query = query.filter(DBFraudAlert.risk_level == risk_level)
            
            query = query.order_by(DBFraudAlert.risk_score.desc()).limit(limit)
            alerts = query.all()
            
            return [self._format_db_alert(alert) for alert in alerts]
            
        except Exception as e:
            print(f"Error getting active alerts: {e}")
            return []
    
    def get_alert_details(self, alert_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific alert.
        """
        try:
            alert = self.db_session.query(DBFraudAlert).filter(
                DBFraudAlert.id == alert_id
            ).first()
            
            if not alert:
                return None
            
            # Get investigation details if available
            investigation = self.fraud_agent.investigate_alert(alert_id)
            
            alert_data = self._format_db_alert(alert)
            alert_data["investigation"] = investigation
            
            return alert_data
            
        except Exception as e:
            print(f"Error getting alert details: {e}")
            return None
    
    def update_alert_status(self, alert_id: str, status: str, resolved_by: str = None, notes: str = None) -> bool:
        """
        Update the status of a fraud alert.
        """
        try:
            alert = self.db_session.query(DBFraudAlert).filter(
                DBFraudAlert.id == alert_id
            ).first()
            
            if not alert:
                return False
            
            alert.status = status
            alert.updated_at = datetime.utcnow()
            
            if status in ["resolved", "false_positive"]:
                alert.resolved_at = datetime.utcnow()
                alert.resolved_by = resolved_by
                alert.resolution_notes = notes
            
            self.db_session.commit()
            return True
            
        except Exception as e:
            print(f"Error updating alert status: {e}")
            self.db_session.rollback()
            return False
    
    def get_fraud_statistics(self, days: int = 30) -> Dict[str, Any]:
        """
        Get fraud detection statistics for the specified period.
        """
        try:
            # Get statistics from database
            start_date = datetime.utcnow() - timedelta(days=days)
            
            stats_query = self.db_session.query(FraudStatistics).filter(
                FraudStatistics.date >= start_date
            ).all()
            
            if not stats_query:
                # Generate current statistics
                return self._generate_current_statistics()
            
            # Aggregate statistics
            total_alerts = sum(s.total_alerts for s in stats_query)
            critical_alerts = sum(s.critical_alerts for s in stats_query)
            high_risk_alerts = sum(s.high_risk_alerts for s in stats_query)
            confirmed_fraud = sum(s.confirmed_fraud for s in stats_query)
            false_positives = sum(s.false_positives for s in stats_query)
            
            return {
                "period_days": days,
                "total_alerts": total_alerts,
                "critical_alerts": critical_alerts,
                "high_risk_alerts": high_risk_alerts,
                "confirmed_fraud": confirmed_fraud,
                "false_positives": false_positives,
                "accuracy_rate": (confirmed_fraud / max(total_alerts, 1)) * 100,
                "false_positive_rate": (false_positives / max(total_alerts, 1)) * 100,
                "avg_detection_time": sum(s.avg_detection_time for s in stats_query) / len(stats_query) if stats_query else 0,
                "fraud_types": self._aggregate_fraud_types(stats_query)
            }
            
        except Exception as e:
            print(f"Error getting fraud statistics: {e}")
            return self._generate_current_statistics()
    
    def create_user_behavior_profile(self, user_id: str) -> bool:
        """
        Create or update user behavior profile for fraud detection.
        """
        try:
            # Get user transaction data
            with self.db_engine.connect() as conn:
                user_query = text("""
                    SELECT 
                        COUNT(*) as transaction_count,
                        AVG(amount) as avg_amount,
                        GROUP_CONCAT(DISTINCT product) as products
                    FROM orders 
                    WHERE id LIKE :user_pattern
                    AND date >= date('now', '-30 days')
                """)
                
                result = conn.execute(user_query, {"user_pattern": f"%{user_id}%"})
                user_data = result.fetchone()
                
                if user_data and user_data[0] > 0:  # Has transactions
                    # Check if profile exists
                    existing_profile = self.db_session.query(UserBehaviorProfile).filter(
                        UserBehaviorProfile.user_id == user_id
                    ).first()
                    
                    if existing_profile:
                        # Update existing profile
                        existing_profile.avg_transaction_amount = float(user_data[1] or 0)
                        existing_profile.transaction_frequency = float(user_data[0]) / 30  # per day
                        existing_profile.common_products = user_data[2].split(',') if user_data[2] else []
                        existing_profile.last_updated = datetime.utcnow()
                    else:
                        # Create new profile
                        profile = UserBehaviorProfile(
                            user_id=user_id,
                            avg_transaction_amount=float(user_data[1] or 0),
                            transaction_frequency=float(user_data[0]) / 30,
                            common_products=user_data[2].split(',') if user_data[2] else [],
                            typical_login_hours=[9, 10, 11, 14, 15, 16],  # Default business hours
                            last_updated=datetime.utcnow()
                        )
                        self.db_session.add(profile)
                    
                    self.db_session.commit()
                    return True
                
                return False
                
        except Exception as e:
            print(f"Error creating user behavior profile: {e}")
            self.db_session.rollback()
            return False
    
    def check_real_time_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform real-time fraud check on a transaction.
        """
        try:
            risk_score = 0
            risk_factors = []
            
            # Check transaction amount
            user_id = transaction_data.get("user_id")
            amount = float(transaction_data.get("amount", 0))
            
            if user_id:
                profile = self.db_session.query(UserBehaviorProfile).filter(
                    UserBehaviorProfile.user_id == user_id
                ).first()
                
                if profile:
                    # Check for amount anomaly
                    if amount > profile.avg_transaction_amount * 5:  # 5x normal amount
                        risk_score += 30
                        risk_factors.append("Transaction amount significantly higher than user's average")
                    
                    # Check transaction frequency
                    # This would require more complex logic to track recent transactions
                    
            # Check for suspicious patterns
            product = transaction_data.get("product", "")
            if "test" in product.lower() or "fake" in product.lower():
                risk_score += 50
                risk_factors.append("Suspicious product name detected")
            
            # Determine risk level
            if risk_score >= 70:
                risk_level = "high"
            elif risk_score >= 40:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            return {
                "transaction_id": transaction_data.get("id"),
                "risk_score": risk_score,
                "risk_level": risk_level,
                "risk_factors": risk_factors,
                "approved": risk_score < 70,
                "requires_review": risk_score >= 40,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "transaction_id": transaction_data.get("id"),
                "risk_score": 0,
                "risk_level": "unknown",
                "risk_factors": [f"Error in fraud check: {str(e)}"],
                "approved": True,
                "requires_review": False,
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def _save_alerts_to_db(self, alerts: List[Dict[str, Any]]):
        """Save fraud alerts to database."""
        try:
            for alert_data in alerts:
                # Check if alert already exists
                existing = self.db_session.query(DBFraudAlert).filter(
                    DBFraudAlert.id == alert_data["id"]
                ).first()
                
                if not existing:
                    db_alert = DBFraudAlert(
                        id=alert_data["id"],
                        fraud_type=alert_data["type"],
                        risk_level=alert_data["risk_level"],
                        risk_score=alert_data["risk_score"],
                        title=alert_data["title"],
                        description=alert_data["description"],
                        evidence=alert_data["evidence"],
                        affected_entities=alert_data["affected_entities"],
                        recommended_actions=alert_data["recommended_actions"],
                        confidence=alert_data["confidence"],
                        ethiopian_context=alert_data.get("ethiopian_context"),
                        status="active"
                    )
                    self.db_session.add(db_alert)
            
            self.db_session.commit()
            
        except Exception as e:
            print(f"Error saving alerts to database: {e}")
            self.db_session.rollback()
    
    def _update_fraud_statistics(self, scan_results: Dict[str, Any]):
        """Update daily fraud statistics."""
        try:
            today = datetime.utcnow().date()
            
            # Check if statistics for today already exist
            existing_stats = self.db_session.query(FraudStatistics).filter(
                FraudStatistics.date >= datetime.combine(today, datetime.min.time())
            ).first()
            
            if existing_stats:
                # Update existing statistics
                existing_stats.total_alerts = scan_results.get("alerts_found", 0)
                existing_stats.critical_alerts = scan_results.get("critical_alerts", 0)
                existing_stats.high_risk_alerts = scan_results.get("high_risk_alerts", 0)
            else:
                # Create new statistics record
                stats = FraudStatistics(
                    date=datetime.utcnow(),
                    total_alerts=scan_results.get("alerts_found", 0),
                    critical_alerts=scan_results.get("critical_alerts", 0),
                    high_risk_alerts=scan_results.get("high_risk_alerts", 0),
                    fraud_types_detected=self._count_fraud_types(scan_results.get("alerts", []))
                )
                self.db_session.add(stats)
            
            self.db_session.commit()
            
        except Exception as e:
            print(f"Error updating fraud statistics: {e}")
            self.db_session.rollback()
    
    def _format_db_alert(self, alert: DBFraudAlert) -> Dict[str, Any]:
        """Format database alert for API response."""
        return {
            "id": alert.id,
            "type": alert.fraud_type,
            "risk_level": alert.risk_level,
            "risk_score": alert.risk_score,
            "title": alert.title,
            "description": alert.description,
            "evidence": alert.evidence,
            "affected_entities": alert.affected_entities,
            "recommended_actions": alert.recommended_actions,
            "confidence": alert.confidence,
            "status": alert.status,
            "ethiopian_context": alert.ethiopian_context,
            "created_at": alert.created_at.isoformat() if alert.created_at else None,
            "updated_at": alert.updated_at.isoformat() if alert.updated_at else None,
            "resolved_at": alert.resolved_at.isoformat() if alert.resolved_at else None,
            "resolved_by": alert.resolved_by,
            "resolution_notes": alert.resolution_notes
        }
    
    def _generate_current_statistics(self) -> Dict[str, Any]:
        """Generate current fraud statistics from active alerts."""
        try:
            active_alerts = self.get_active_alerts()
            
            total_alerts = len(active_alerts)
            critical_alerts = len([a for a in active_alerts if a["risk_level"] == "critical"])
            high_risk_alerts = len([a for a in active_alerts if a["risk_level"] == "high"])
            
            fraud_types = {}
            for alert in active_alerts:
                fraud_type = alert["type"]
                fraud_types[fraud_type] = fraud_types.get(fraud_type, 0) + 1
            
            return {
                "period_days": 1,
                "total_alerts": total_alerts,
                "critical_alerts": critical_alerts,
                "high_risk_alerts": high_risk_alerts,
                "confirmed_fraud": 0,
                "false_positives": 0,
                "accuracy_rate": 0,
                "false_positive_rate": 0,
                "avg_detection_time": 0,
                "fraud_types": fraud_types
            }
            
        except Exception as e:
            print(f"Error generating current statistics: {e}")
            return {
                "period_days": 1,
                "total_alerts": 0,
                "critical_alerts": 0,
                "high_risk_alerts": 0,
                "confirmed_fraud": 0,
                "false_positives": 0,
                "accuracy_rate": 0,
                "false_positive_rate": 0,
                "avg_detection_time": 0,
                "fraud_types": {}
            }
    
    def _count_fraud_types(self, alerts: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count fraud types from alerts list."""
        fraud_types = {}
        for alert in alerts:
            fraud_type = alert.get("type", "unknown")
            fraud_types[fraud_type] = fraud_types.get(fraud_type, 0) + 1
        return fraud_types
    
    def _aggregate_fraud_types(self, stats_list: List[FraudStatistics]) -> Dict[str, int]:
        """Aggregate fraud types from statistics records."""
        aggregated = {}
        for stats in stats_list:
            if stats.fraud_types_detected:
                for fraud_type, count in stats.fraud_types_detected.items():
                    aggregated[fraud_type] = aggregated.get(fraud_type, 0) + count
        return aggregated
    
    def __del__(self):
        """Clean up database session."""
        if hasattr(self, 'db_session'):
            self.db_session.close()