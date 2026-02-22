import os
import json
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from sqlalchemy import text, create_engine
import numpy as np
from collections import defaultdict
import hashlib

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class FraudType(Enum):
    PRICING_MANIPULATION = "pricing_manipulation"
    ACCOUNT_FRAUD = "account_fraud"
    TRANSACTION_FRAUD = "transaction_fraud"
    INVENTORY_FRAUD = "inventory_fraud"
    COORDINATED_ATTACK = "coordinated_attack"

class AlertStatus(Enum):
    ACTIVE = "active"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"

@dataclass
class FraudAlert:
    id: str
    fraud_type: FraudType
    risk_level: RiskLevel
    risk_score: float
    title: str
    description: str
    evidence: Dict[str, Any]
    affected_entities: List[str]  # user_ids, product_ids, etc.
    recommended_actions: List[str]
    confidence: float
    timestamp: datetime
    status: AlertStatus = AlertStatus.ACTIVE
    ethiopian_context: Optional[str] = None

@dataclass
class UserBehaviorProfile:
    user_id: str
    avg_transaction_amount: float
    avg_session_duration: float
    typical_login_hours: List[int]
    common_products: List[str]
    transaction_frequency: float
    last_updated: datetime

class FraudDetectionEngine:
    """
    Core fraud detection engine that analyzes patterns and generates alerts.
    """
    
    def __init__(self, db_engine, api_key: Optional[str] = None):
        self.db_engine = db_engine
        self.api_key = api_key or os.getenv("API_KEY")
        
        if self.api_key:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=self.api_key,
                temperature=0.2
            )
        else:
            self.llm = None
        
        # Ethiopian market context
        self.ethiopian_holidays = [
            "Meskel", "Timkat", "Fasika", "Enkutatash", "Genna"
        ]
        
        # Seasonal patterns for Ethiopian products
        self.seasonal_patterns = {
            "teff": {"harvest_months": [10, 11, 12], "price_variation": 0.3},
            "coffee": {"harvest_months": [10, 11, 12, 1], "price_variation": 0.25},
            "honey": {"harvest_months": [11, 12, 1], "price_variation": 0.2},
            "berbere": {"peak_months": [9, 10, 11], "price_variation": 0.15}
        }
        
        # Risk thresholds
        self.risk_thresholds = {
            "price_spike": 0.5,  # 50% price increase
            "price_drop": 0.4,   # 40% price decrease
            "transaction_volume": 10,  # 10x normal volume
            "login_anomaly": 0.8,     # 80% deviation from normal pattern
            "inventory_manipulation": 0.6  # 60% stock change
        }

    def analyze_pricing_patterns(self) -> List[FraudAlert]:
        """Detect pricing manipulation and abnormal pricing patterns."""
        alerts = []
        
        try:
            with self.db_engine.connect() as conn:
                # Get recent pricing data
                pricing_query = text("""
                    SELECT p.id, p.name, p.price, p.category, p.seller,
                           LAG(p.price) OVER (PARTITION BY p.id ORDER BY p.id) as prev_price
                    FROM products p
                    ORDER BY p.id
                """)
                
                result = conn.execute(pricing_query)
                products = [dict(row._mapping) for row in result]
                
                for product in products:
                    if product['prev_price'] and product['price']:
                        price_change = (product['price'] - product['prev_price']) / product['prev_price']
                        
                        # Check for abnormal price spikes
                        if abs(price_change) > self.risk_thresholds['price_spike']:
                            risk_score = min(100, abs(price_change) * 100)
                            risk_level = self._calculate_risk_level(risk_score)
                            
                            # Check if it's legitimate seasonal variation
                            is_seasonal = self._is_seasonal_variation(product['name'], price_change)
                            
                            if not is_seasonal:
                                alert = FraudAlert(
                                    id=f"PRICE_{product['id']}_{int(datetime.now().timestamp())}",
                                    fraud_type=FraudType.PRICING_MANIPULATION,
                                    risk_level=risk_level,
                                    risk_score=risk_score,
                                    title=f"Suspicious price change: {product['name']}",
                                    description=f"Price changed by {price_change*100:.1f}% from {product['prev_price']} to {product['price']} ETB",
                                    evidence={
                                        "product_id": product['id'],
                                        "old_price": product['prev_price'],
                                        "new_price": product['price'],
                                        "change_percentage": price_change * 100,
                                        "seller": product['seller']
                                    },
                                    affected_entities=[str(product['id'])],
                                    recommended_actions=[
                                        "Review seller's pricing history",
                                        "Contact seller for explanation",
                                        "Monitor for coordinated pricing with other sellers",
                                        "Check for inventory manipulation"
                                    ],
                                    confidence=0.8 if abs(price_change) > 0.7 else 0.6,
                                    timestamp=datetime.now(),
                                    ethiopian_context=self._get_ethiopian_pricing_context(product['name'])
                                )
                                alerts.append(alert)
                
        except Exception as e:
            print(f"Error analyzing pricing patterns: {e}")
        
        return alerts

    def analyze_transaction_patterns(self) -> List[FraudAlert]:
        """Detect unusual transaction patterns and potential fraud."""
        alerts = []
        
        try:
            with self.db_engine.connect() as conn:
                # Get recent transaction data
                transaction_query = text("""
                    SELECT o.id, o.product, o.amount, o.status, o.date,
                           COUNT(*) OVER (PARTITION BY o.product) as product_order_count,
                           AVG(o.amount) OVER (PARTITION BY o.product) as avg_amount
                    FROM orders o
                    WHERE o.date >= date('now', '-30 days')
                    ORDER BY o.date DESC
                """)
                
                result = conn.execute(transaction_query)
                transactions = [dict(row._mapping) for row in result]
                
                # Analyze for wash trading and artificial inflation
                product_transactions = defaultdict(list)
                for tx in transactions:
                    product_transactions[tx['product']].append(tx)
                
                for product, txs in product_transactions.items():
                    if len(txs) > 20:  # High transaction volume
                        # Check for suspicious patterns
                        amounts = [tx['amount'] for tx in txs]
                        avg_amount = np.mean(amounts)
                        std_amount = np.std(amounts)
                        
                        # Look for repeated identical amounts (wash trading indicator)
                        amount_counts = defaultdict(int)
                        for amount in amounts:
                            amount_counts[amount] += 1
                        
                        max_identical = max(amount_counts.values())
                        if max_identical > len(txs) * 0.3:  # 30% of transactions are identical
                            risk_score = min(100, (max_identical / len(txs)) * 100)
                            
                            alert = FraudAlert(
                                id=f"WASH_{hashlib.md5(product.encode()).hexdigest()[:8]}_{int(datetime.now().timestamp())}",
                                fraud_type=FraudType.TRANSACTION_FRAUD,
                                risk_level=self._calculate_risk_level(risk_score),
                                risk_score=risk_score,
                                title=f"Potential wash trading detected: {product}",
                                description=f"Found {max_identical} identical transactions of {list(amount_counts.keys())[0]} ETB out of {len(txs)} total transactions",
                                evidence={
                                    "product": product,
                                    "total_transactions": len(txs),
                                    "identical_amount_count": max_identical,
                                    "suspicious_amount": list(amount_counts.keys())[0],
                                    "pattern_percentage": (max_identical / len(txs)) * 100
                                },
                                affected_entities=[product],
                                recommended_actions=[
                                    "Investigate transaction origins",
                                    "Check for coordinated buyer accounts",
                                    "Review payment methods",
                                    "Temporarily flag product for monitoring"
                                ],
                                confidence=0.9 if risk_score > 70 else 0.7,
                                timestamp=datetime.now()
                            )
                            alerts.append(alert)
                
        except Exception as e:
            print(f"Error analyzing transaction patterns: {e}")
        
        return alerts

    def analyze_inventory_patterns(self) -> List[FraudAlert]:
        """Detect inventory manipulation and phantom stock."""
        alerts = []
        
        try:
            with self.db_engine.connect() as conn:
                # Get products with suspicious stock patterns
                inventory_query = text("""
                    SELECT p.id, p.name, p.stock, p.seller, p.category,
                           COUNT(o.id) as recent_orders
                    FROM products p
                    LEFT JOIN orders o ON p.name = o.product 
                        AND o.date >= date('now', '-7 days')
                    GROUP BY p.id, p.name, p.stock, p.seller, p.category
                    HAVING p.stock > 0
                """)
                
                result = conn.execute(inventory_query)
                products = [dict(row._mapping) for row in result]
                
                for product in products:
                    # Check for phantom inventory (high stock, no recent orders)
                    if product['stock'] > 100 and product['recent_orders'] == 0:
                        risk_score = min(100, (product['stock'] / 10))
                        
                        alert = FraudAlert(
                            id=f"INV_{product['id']}_{int(datetime.now().timestamp())}",
                            fraud_type=FraudType.INVENTORY_FRAUD,
                            risk_level=self._calculate_risk_level(risk_score),
                            risk_score=risk_score,
                            title=f"Potential phantom inventory: {product['name']}",
                            description=f"High stock ({product['stock']} units) with no recent orders in 7 days",
                            evidence={
                                "product_id": product['id'],
                                "stock_level": product['stock'],
                                "recent_orders": product['recent_orders'],
                                "seller": product['seller']
                            },
                            affected_entities=[str(product['id'])],
                            recommended_actions=[
                                "Verify actual inventory with seller",
                                "Request proof of stock photos",
                                "Check seller's fulfillment history",
                                "Monitor for bait-and-switch patterns"
                            ],
                            confidence=0.7,
                            timestamp=datetime.now(),
                            ethiopian_context="Consider traditional storage methods and seasonal stockpiling practices"
                        )
                        alerts.append(alert)
                
        except Exception as e:
            print(f"Error analyzing inventory patterns: {e}")
        
        return alerts

    def detect_coordinated_attacks(self) -> List[FraudAlert]:
        """Detect coordinated fraud attempts across multiple accounts/products."""
        alerts = []
        
        try:
            with self.db_engine.connect() as conn:
                # Look for coordinated pricing changes
                pricing_query = text("""
                    SELECT seller, category, COUNT(*) as product_count,
                           AVG(price) as avg_price, MIN(price) as min_price, MAX(price) as max_price
                    FROM products
                    GROUP BY seller, category
                    HAVING COUNT(*) > 1
                """)
                
                result = conn.execute(pricing_query)
                seller_data = [dict(row._mapping) for row in result]
                
                # Check for suspicious seller patterns
                for seller in seller_data:
                    price_range = seller['max_price'] - seller['min_price']
                    if price_range == 0 and seller['product_count'] > 3:
                        # All products have identical pricing - suspicious
                        risk_score = min(100, seller['product_count'] * 15)
                        
                        alert = FraudAlert(
                            id=f"COORD_{hashlib.md5(seller['seller'].encode()).hexdigest()[:8]}_{int(datetime.now().timestamp())}",
                            fraud_type=FraudType.COORDINATED_ATTACK,
                            risk_level=self._calculate_risk_level(risk_score),
                            risk_score=risk_score,
                            title=f"Coordinated pricing detected: {seller['seller']}",
                            description=f"Seller has {seller['product_count']} products all priced identically at {seller['avg_price']} ETB",
                            evidence={
                                "seller": seller['seller'],
                                "product_count": seller['product_count'],
                                "identical_price": seller['avg_price'],
                                "category": seller['category']
                            },
                            affected_entities=[seller['seller']],
                            recommended_actions=[
                                "Review seller's account creation date",
                                "Check for duplicate seller information",
                                "Investigate pricing strategy rationale",
                                "Monitor for coordinated inventory changes"
                            ],
                            confidence=0.8,
                            timestamp=datetime.now()
                        )
                        alerts.append(alert)
                
        except Exception as e:
            print(f"Error detecting coordinated attacks: {e}")
        
        return alerts

    def _calculate_risk_level(self, risk_score: float) -> RiskLevel:
        """Convert risk score to risk level."""
        if risk_score >= 80:
            return RiskLevel.CRITICAL
        elif risk_score >= 60:
            return RiskLevel.HIGH
        elif risk_score >= 30:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW

    def _is_seasonal_variation(self, product_name: str, price_change: float) -> bool:
        """Check if price change is due to legitimate seasonal variation."""
        current_month = datetime.now().month
        
        for product_key, pattern in self.seasonal_patterns.items():
            if product_key.lower() in product_name.lower():
                if current_month in pattern['harvest_months']:
                    # During harvest, prices typically drop
                    return price_change < 0 and abs(price_change) <= pattern['price_variation']
                else:
                    # Off-season, prices may increase
                    return abs(price_change) <= pattern['price_variation']
        
        return False

    def _get_ethiopian_pricing_context(self, product_name: str) -> str:
        """Provide Ethiopian market context for pricing alerts."""
        current_month = datetime.now().month
        
        contexts = []
        
        # Check for seasonal context
        for product_key, pattern in self.seasonal_patterns.items():
            if product_key.lower() in product_name.lower():
                if current_month in pattern['harvest_months']:
                    contexts.append(f"Currently in {product_key} harvest season - price drops may be normal")
                else:
                    contexts.append(f"Off-season for {product_key} - price increases may be expected")
        
        # Add general Ethiopian market context
        if current_month in [9, 10]:  # Around Meskel
            contexts.append("Meskel season - increased demand for traditional products expected")
        elif current_month in [1, 2]:  # Around Timkat
            contexts.append("Timkat season - holiday demand patterns may affect pricing")
        
        return "; ".join(contexts) if contexts else "Consider Ethiopian seasonal and cultural factors"

class FraudDetectionAgent:
    """
    Main Fraud Detection Agent that coordinates detection, analysis, and response.
    """
    
    def __init__(self, sql_agent=None, rag_agent=None, api_key: Optional[str] = None):
        self.sql_agent = sql_agent
        self.rag_agent = rag_agent
        self.api_key = api_key or os.getenv("API_KEY")
        
        if self.api_key:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=self.api_key,
                temperature=0.3
            )
        else:
            self.llm = None
        
        # Initialize fraud detection engine
        if sql_agent and hasattr(sql_agent, 'engine'):
            self.engine = FraudDetectionEngine(sql_agent.engine, api_key)
        else:
            self.engine = None
        
        # Initialize fraud alert storage
        self.active_alerts: List[FraudAlert] = []

    def run_fraud_scan(self, scan_type: str = "full") -> Dict[str, Any]:
        """
        Run comprehensive fraud detection scan.
        """
        if not self.engine:
            return {
                "status": "error",
                "message": "Fraud detection engine not initialized - database connection required",
                "alerts": [],
                "summary": ""
            }
        
        try:
            all_alerts = []
            
            # Run different types of scans based on request
            if scan_type in ["full", "pricing"]:
                pricing_alerts = self.engine.analyze_pricing_patterns()
                all_alerts.extend(pricing_alerts)
            
            if scan_type in ["full", "transactions"]:
                transaction_alerts = self.engine.analyze_transaction_patterns()
                all_alerts.extend(transaction_alerts)
            
            if scan_type in ["full", "inventory"]:
                inventory_alerts = self.engine.analyze_inventory_patterns()
                all_alerts.extend(inventory_alerts)
            
            if scan_type in ["full", "coordinated"]:
                coordinated_alerts = self.engine.detect_coordinated_attacks()
                all_alerts.extend(coordinated_alerts)
            
            # Sort alerts by risk score
            all_alerts.sort(key=lambda x: x.risk_score, reverse=True)
            
            # Update active alerts
            self.active_alerts = all_alerts
            
            # Generate summary
            summary = self._generate_fraud_summary(all_alerts)
            
            # Format alerts for response
            formatted_alerts = []
            for alert in all_alerts:
                formatted_alerts.append({
                    "id": alert.id,
                    "type": alert.fraud_type.value,
                    "risk_level": alert.risk_level.value,
                    "risk_score": alert.risk_score,
                    "title": alert.title,
                    "description": alert.description,
                    "evidence": alert.evidence,
                    "affected_entities": alert.affected_entities,
                    "recommended_actions": alert.recommended_actions,
                    "confidence": alert.confidence,
                    "timestamp": alert.timestamp.isoformat(),
                    "ethiopian_context": alert.ethiopian_context
                })
            
            return {
                "status": "success",
                "scan_type": scan_type,
                "alerts_found": len(all_alerts),
                "critical_alerts": len([a for a in all_alerts if a.risk_level == RiskLevel.CRITICAL]),
                "high_risk_alerts": len([a for a in all_alerts if a.risk_level == RiskLevel.HIGH]),
                "alerts": formatted_alerts,
                "summary": summary,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error during fraud scan: {str(e)}",
                "alerts": [],
                "summary": ""
            }

    def investigate_alert(self, alert_id: str) -> Dict[str, Any]:
        """
        Provide detailed investigation information for a specific alert.
        """
        alert = next((a for a in self.active_alerts if a.id == alert_id), None)
        
        if not alert:
            return {
                "status": "error",
                "message": f"Alert {alert_id} not found"
            }
        
        try:
            # Generate detailed investigation report
            investigation = self._generate_investigation_report(alert)
            
            return {
                "status": "success",
                "alert_id": alert_id,
                "investigation": investigation,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error investigating alert: {str(e)}"
            }

    def _generate_fraud_summary(self, alerts: List[FraudAlert]) -> str:
        """Generate human-readable summary of fraud detection results."""
        if not alerts:
            return "No fraud indicators detected in current scan. All marketplace activities appear normal."
        
        if not self.llm:
            return f"Detected {len(alerts)} potential fraud indicators requiring investigation."
        
        try:
            # Prepare alert summary for LLM
            alert_summary = []
            for alert in alerts[:5]:  # Top 5 alerts
                alert_summary.append(f"""
Type: {alert.fraud_type.value}
Risk: {alert.risk_level.value} ({alert.risk_score:.1f}/100)
Issue: {alert.title}
Details: {alert.description}
Confidence: {alert.confidence:.1f}
""")
            
            template = """
You are a fraud detection specialist for the Ethiopian marketplace. 

Fraud Detection Results:
{alert_summary}

Total alerts: {total_alerts}
Critical/High risk: {critical_count}

FORMATTING RULES:
- Write in plain text only, no markdown, asterisks, or bullet points
- Use a professional but accessible tone
- Focus on actionable insights
- Consider Ethiopian market context

Provide a clear summary that:
1. Highlights the most serious threats
2. Explains the business impact
3. Recommends immediate actions
4. Considers Ethiopian market patterns

Summary:"""
            
            prompt = PromptTemplate(template=template, input_variables=["alert_summary", "total_alerts", "critical_count"])
            chain = prompt | self.llm
            
            critical_count = len([a for a in alerts if a.risk_level in [RiskLevel.CRITICAL, RiskLevel.HIGH]])
            
            result = chain.invoke({
                "alert_summary": "\n".join(alert_summary),
                "total_alerts": len(alerts),
                "critical_count": critical_count
            })
            
            return result.content
            
        except Exception as e:
            error_message = str(e).lower()
            
            if "resource_exhausted" in error_message or "quota" in error_message or "429" in error_message:
                critical_count = len([a for a in alerts if a.risk_level == RiskLevel.CRITICAL])
                return f"Fraud Detection Agent experienced a technical hurdle. Detected {len(alerts)} fraud indicators with {critical_count} critical alerts requiring immediate attention. AI summary temporarily unavailable due to high system demand."
            else:
                return f"Detected {len(alerts)} fraud indicators. {len([a for a in alerts if a.risk_level == RiskLevel.CRITICAL])} critical alerts require immediate attention."

    def _generate_investigation_report(self, alert: FraudAlert) -> Dict[str, Any]:
        """Generate detailed investigation report for an alert."""
        if not self.llm:
            return {
                "summary": f"Alert {alert.id} requires manual investigation",
                "next_steps": alert.recommended_actions,
                "evidence": alert.evidence
            }
        
        try:
            template = """
You are investigating a fraud alert for the Ethiopian marketplace.

Alert Details:
Type: {fraud_type}
Risk Level: {risk_level}
Title: {title}
Description: {description}
Evidence: {evidence}
Ethiopian Context: {ethiopian_context}

FORMATTING RULES:
- Write in plain text only, no markdown formatting
- Be thorough but concise
- Focus on actionable investigation steps

Provide a detailed investigation report including:
1. Risk assessment and potential impact
2. Specific evidence to collect
3. Investigation priorities
4. Ethiopian market considerations

Investigation Report:"""
            
            prompt = PromptTemplate(template=template, input_variables=[
                "fraud_type", "risk_level", "title", "description", "evidence", "ethiopian_context"
            ])
            chain = prompt | self.llm
            
            result = chain.invoke({
                "fraud_type": alert.fraud_type.value,
                "risk_level": alert.risk_level.value,
                "title": alert.title,
                "description": alert.description,
                "evidence": json.dumps(alert.evidence, indent=2),
                "ethiopian_context": alert.ethiopian_context or "Standard market analysis"
            })
            
            return {
                "summary": result.content,
                "next_steps": alert.recommended_actions,
                "evidence": alert.evidence,
                "confidence": alert.confidence,
                "ethiopian_context": alert.ethiopian_context
            }
            
        except Exception as e:
            error_message = str(e).lower()
            
            if "resource_exhausted" in error_message or "quota" in error_message or "429" in error_message:
                return {
                    "summary": f"Fraud Detection Agent experienced a technical hurdle. Alert {alert.id} requires investigation. AI analysis temporarily unavailable due to high system demand.",
                    "next_steps": alert.recommended_actions,
                    "evidence": alert.evidence
                }
            else:
                return {
                    "summary": f"Investigation report generation encountered an issue. Alert {alert.id} requires manual review.",
                    "next_steps": alert.recommended_actions,
                    "evidence": alert.evidence
                }

    def get_fraud_statistics(self) -> Dict[str, Any]:
        """Get fraud detection statistics and trends."""
        if not self.active_alerts:
            return {
                "total_alerts": 0,
                "risk_distribution": {},
                "fraud_types": {},
                "trends": "No recent fraud activity detected"
            }
        
        # Calculate statistics
        risk_distribution = defaultdict(int)
        fraud_types = defaultdict(int)
        
        for alert in self.active_alerts:
            risk_distribution[alert.risk_level.value] += 1
            fraud_types[alert.fraud_type.value] += 1
        
        return {
            "total_alerts": len(self.active_alerts),
            "risk_distribution": dict(risk_distribution),
            "fraud_types": dict(fraud_types),
            "avg_risk_score": np.mean([a.risk_score for a in self.active_alerts]),
            "avg_confidence": np.mean([a.confidence for a in self.active_alerts]),
            "last_scan": datetime.now().isoformat()
        }