import os
import json
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from sqlalchemy import text

class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class RecommendationType(Enum):
    PRICING = "pricing"
    DEMAND_FORECAST = "demand_forecast"
    INVENTORY = "inventory"
    MARKET_OPPORTUNITY = "market_opportunity"

@dataclass
class Recommendation:
    type: RecommendationType
    priority: Priority
    title: str
    description: str
    impact_score: float
    confidence: float
    data_points: Dict
    action_items: List[str]
    seller_filter: Optional[str] = None

class RecommendationEngine:
    """
    Advanced Recommendation Engine for Marketplace AI.
    Analyzes transaction patterns, pricing trends, and market dynamics
    to generate actionable insights for sellers and market owners.
    """
    
    def __init__(self, db_engine, api_key: Optional[str] = None):
        self.db_engine = db_engine
        self.api_key = api_key or os.getenv("API_KEY")
        
        if self.api_key:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=self.api_key,
                temperature=0.3
            )
        else:
            self.llm = None

    def analyze_market_trends(self) -> Dict:
        """Analyze current market trends from database."""
        try:
            with self.db_engine.connect() as conn:
                # Get product performance data
                products_query = text("SELECT * FROM products ORDER BY rating DESC, stock ASC")
                products_result = conn.execute(products_query)
                products = [dict(row._mapping) for row in products_result]
                
                # Get order trends
                orders_query = text("SELECT * FROM orders ORDER BY date DESC LIMIT 10")
                orders_result = conn.execute(orders_query)
                orders = [dict(row._mapping) for row in orders_result]
                
                return {
                    "products": products,
                    "orders": orders,
                    "total_products": len(products),
                    "recent_orders": len(orders)
                }
        except Exception as e:
            print(f"Error analyzing market trends: {e}")
            return {"products": [], "orders": [], "total_products": 0, "recent_orders": 0}

    def generate_pricing_recommendations(self, market_data: Dict) -> List[Recommendation]:
        """Generate pricing strategy recommendations."""
        recommendations = []
        
        for product in market_data.get("products", []):
            if product["stock"] < 20:  # Low stock
                rec = Recommendation(
                    type=RecommendationType.PRICING,
                    priority=Priority.HIGH,
                    title=f"Increase price for {product['name']}",
                    description=f"Low stock ({product['stock']} units) suggests high demand. Consider 10-15% price increase.",
                    impact_score=0.8,
                    confidence=0.9,
                    data_points={"current_stock": product["stock"], "current_price": product["price"]},
                    action_items=[
                        f"Increase price from ${product['price']} to ${product['price'] * 1.1:.2f}",
                        "Monitor demand response over next 7 days",
                        "Prepare restock plan"
                    ]
                )
                recommendations.append(rec)
            elif product["stock"] > 100:  # High stock
                rec = Recommendation(
                    type=RecommendationType.PRICING,
                    priority=Priority.MEDIUM,
                    title=f"Consider promotional pricing for {product['name']}",
                    description=f"High stock ({product['stock']} units) suggests slow movement. Consider promotional pricing.",
                    impact_score=0.6,
                    confidence=0.7,
                    data_points={"current_stock": product["stock"], "current_price": product["price"]},
                    action_items=[
                        f"Reduce price by 5-10% to ${product['price'] * 0.9:.2f}",
                        "Create bundle offers",
                        "Launch targeted marketing campaign"
                    ]
                )
                recommendations.append(rec)
        
        return recommendations

    def generate_inventory_recommendations(self, market_data: Dict) -> List[Recommendation]:
        """Generate inventory management recommendations."""
        recommendations = []
        
        # Analyze low stock items
        low_stock_items = [p for p in market_data.get("products", []) if p["stock"] < 20]
        
        if low_stock_items:
            for item in low_stock_items[:3]:  # Top 3 critical items
                rec = Recommendation(
                    type=RecommendationType.INVENTORY,
                    priority=Priority.HIGH,
                    title=f"Urgent restock needed: {item['name']}",
                    description=f"Critical stock level ({item['stock']} units). Restock immediately to avoid stockouts.",
                    impact_score=0.9,
                    confidence=0.95,
                    data_points={"current_stock": item["stock"], "category": item["category"]},
                    action_items=[
                        f"Order minimum 50 units of {item['name']}",
                        "Contact supplier immediately",
                        "Set up automatic reorder point at 25 units"
                    ]
                )
                recommendations.append(rec)
        
        return recommendations

    def generate_demand_forecast(self, market_data: Dict) -> List[Recommendation]:
        """Generate demand forecasting recommendations."""
        recommendations = []
        
        # Analyze recent orders for trends
        recent_orders = market_data.get("orders", [])
        if recent_orders:
            # Count product mentions in recent orders
            product_demand = {}
            for order in recent_orders:
                product = order["product"]
                product_demand[product] = product_demand.get(product, 0) + 1
            
            # Find trending products
            if product_demand:
                top_product = max(product_demand, key=product_demand.get)
                rec = Recommendation(
                    type=RecommendationType.DEMAND_FORECAST,
                    priority=Priority.MEDIUM,
                    title=f"High demand trend detected: {top_product}",
                    description=f"Recent orders show {top_product} is trending with {product_demand[top_product]} orders.",
                    impact_score=0.7,
                    confidence=0.8,
                    data_points={"order_count": product_demand[top_product], "trend_period": "7 days"},
                    action_items=[
                        f"Increase inventory for {top_product}",
                        "Analyze competitor pricing",
                        "Consider expanding product variants"
                    ]
                )
                recommendations.append(rec)
        
        return recommendations

    def generate_market_opportunities(self, market_data: Dict) -> List[Recommendation]:
        """Generate market opportunity recommendations."""
        recommendations = []
        
        # Analyze category distribution
        categories = {}
        for product in market_data.get("products", []):
            cat = product["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        if categories:
            # Find underrepresented categories
            avg_products_per_category = sum(categories.values()) / len(categories)
            
            for category, count in categories.items():
                if count < avg_products_per_category * 0.5:  # Less than half average
                    rec = Recommendation(
                        type=RecommendationType.MARKET_OPPORTUNITY,
                        priority=Priority.LOW,
                        title=f"Expand {category} category",
                        description=f"Only {count} products in {category}. Market opportunity for expansion.",
                        impact_score=0.5,
                        confidence=0.6,
                        data_points={"current_products": count, "category": category},
                        action_items=[
                            f"Research popular {category} products",
                            "Contact suppliers in this category",
                            "Analyze competitor offerings"
                        ]
                    )
                    recommendations.append(rec)
        
        return recommendations

    def format_recommendations_for_llm(self, recommendations: List[Recommendation]) -> str:
        """Format recommendations for LLM processing."""
        if not recommendations:
            return "No specific recommendations generated from current data."
        
        formatted = []
        for rec in recommendations:
            formatted.append(f"""
Type: {rec.type.value}
Priority: {rec.priority.value}
Title: {rec.title}
Description: {rec.description}
Impact Score: {rec.impact_score}
Confidence: {rec.confidence}
Action Items: {', '.join(rec.action_items)}
""")
        
        return "\n".join(formatted)

class RecommendationAgent:
    """
    Main Recommendation Agent that coordinates with other agents and provides
    intelligent business recommendations.
    """
    
    def __init__(self, sql_agent=None, rag_agent=None, api_key: Optional[str] = None):
        self.sql_agent = sql_agent
        self.rag_agent = rag_agent
        self.api_key = api_key or os.getenv("API_KEY")
        
        if self.api_key:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=self.api_key,
                temperature=0.4
            )
        else:
            self.llm = None
        
        # Initialize recommendation engine if we have database access
        if sql_agent and hasattr(sql_agent, 'engine'):
            self.engine = RecommendationEngine(sql_agent.engine, api_key)
        else:
            self.engine = None

    def generate_recommendations(self, query: str, seller_id: Optional[str] = None) -> Dict:
        """
        Main entry point for generating recommendations.
        Analyzes dashboard data, database, and knowledge base to provide comprehensive advice.
        """
        try:
            if not self.engine:
                return {
                    "summary": "Recommendation engine is not properly initialized. Database connection required.",
                    "recommendations": [],
                    "recommendation_type": "ERROR",
                    "ethiopian_context": ""
                }
            
            # 1. Analyze current market data from database
            market_data = self.engine.analyze_market_trends()
            
            # 2. Query knowledge base for relevant insights (if RAG agent available)
            knowledge_insights = ""
            if self.rag_agent:
                try:
                    # Query knowledge base for business advice, market strategies, etc.
                    rag_query = f"Business advice and strategies related to: {query}"
                    rag_result = self.rag_agent.ask(rag_query)
                    
                    if rag_result and "answer" in rag_result:
                        knowledge_insights = rag_result["answer"]
                        print(f"Knowledge base insights retrieved: {len(knowledge_insights)} chars")
                except Exception as e:
                    print(f"Could not retrieve knowledge base insights: {e}")
                    knowledge_insights = ""
            
            # 3. Get additional SQL analytics if needed
            sql_insights = ""
            if self.sql_agent:
                try:
                    # Get comprehensive analytics using the SQL agent's query_inventory method
                    sql_query = "Show me category breakdown with average prices and total stock"
                    sql_result = self.sql_agent.query_inventory(sql_query)
                    sql_insights = f"Category Analytics: {sql_result}"
                except Exception as e:
                    print(f"Could not retrieve SQL insights: {e}")
            
            # 4. Generate different types of recommendations
            all_recommendations = []
            all_recommendations.extend(self.engine.generate_pricing_recommendations(market_data))
            all_recommendations.extend(self.engine.generate_inventory_recommendations(market_data))
            all_recommendations.extend(self.engine.generate_demand_forecast(market_data))
            all_recommendations.extend(self.engine.generate_market_opportunities(market_data))
            
            # Sort by priority and impact
            all_recommendations.sort(key=lambda x: (x.priority.value == "high", x.impact_score), reverse=True)
            
            # Take top 5 recommendations
            top_recommendations = all_recommendations[:5]
            
            # Format for response
            formatted_recs = []
            for rec in top_recommendations:
                formatted_recs.append({
                    "type": rec.type.value,
                    "priority": rec.priority.value,
                    "title": rec.title,
                    "description": rec.description,
                    "impact_score": rec.impact_score,
                    "confidence": rec.confidence,
                    "action_items": rec.action_items
                })
            
            # 5. Generate comprehensive summary using all data sources
            summary = self._generate_comprehensive_summary(
                query, 
                top_recommendations, 
                market_data,
                knowledge_insights,
                sql_insights
            )
            
            return {
                "summary": summary,
                "recommendations": formatted_recs,
                "recommendation_type": "MIXED" if len(set(r.type for r in top_recommendations)) > 1 else top_recommendations[0].type.value if top_recommendations else "GENERAL",
                "ethiopian_context": self._add_ethiopian_context(top_recommendations),
                "data_sources": {
                    "dashboard_analyzed": True,
                    "database_queried": True,
                    "knowledge_base_consulted": bool(knowledge_insights),
                    "total_products_analyzed": market_data.get("total_products", 0),
                    "recent_orders_analyzed": market_data.get("recent_orders", 0)
                }
            }
            
        except Exception as e:
            print(f"Error in generate_recommendations: {e}")
            return {
                "summary": f"Error generating recommendations: {str(e)}",
                "recommendations": [],
                "recommendation_type": "ERROR",
                "ethiopian_context": ""
            }

    def _generate_comprehensive_summary(
        self, 
        query: str, 
        recommendations: List[Recommendation], 
        market_data: Dict,
        knowledge_insights: str = "",
        sql_insights: str = ""
    ) -> str:
        """Generate a comprehensive natural language summary using all available data sources."""
        if not self.llm or not recommendations:
            return f"Generated {len(recommendations)} recommendations based on current market analysis."
        
        try:
            rec_text = self.engine.format_recommendations_for_llm(recommendations)
            
            template = """
            You are an expert business consultant for Ethiopian marketplace sellers with access to multiple data sources.
            
            User asked: "{query}"
            
            DASHBOARD & DATABASE ANALYSIS:
            {recommendations}
            
            Market snapshot: {market_data}
            
            SQL ANALYTICS:
            {sql_insights}
            
            KNOWLEDGE BASE INSIGHTS:
            {knowledge_insights}
            
            CRITICAL FORMATTING RULES:
            - Write in plain text ONLY like you're having a friendly conversation with a colleague
            - NEVER use asterisks (*), bold text (**), bullet points, numbered lists, or any markdown formatting
            - Instead of bullet points, use natural transitions like "First," "Also," "Additionally," "Finally"
            - Write in a warm, conversational tone as if speaking directly to the person
            
            Provide a comprehensive, actionable summary that:
            - Directly addresses the user's question with specific advice
            - Synthesizes insights from dashboard data, database analytics, and knowledge base
            - Highlights the most important recommendations with clear reasoning
            - Considers Ethiopian market context, seasonal factors, and cultural considerations
            - Provides specific numbers and data points when available
            - Suggests concrete next steps the user can take immediately
            - Keeps a professional but warm, human tone
            
            If the knowledge base provided relevant strategies or best practices, incorporate them naturally into your advice.
            
            Comprehensive Advice:"""
            
            prompt = PromptTemplate(
                template=template, 
                input_variables=["query", "recommendations", "market_data", "knowledge_insights", "sql_insights"]
            )
            chain = prompt | self.llm
            
            result = chain.invoke({
                "query": query,
                "recommendations": rec_text,
                "market_data": str(market_data),
                "knowledge_insights": knowledge_insights or "No additional knowledge base insights available.",
                "sql_insights": sql_insights or "No additional SQL analytics available."
            })
            
            return result.content
            
        except Exception as e:
            error_message = str(e).lower()
            
            if "resource_exhausted" in error_message or "quota" in error_message or "429" in error_message:
                return f"Recommendation Engine experienced a technical hurdle. Generated {len(recommendations)} recommendations but AI summary is temporarily unavailable due to high system demand."
            else:
                return f"Generated {len(recommendations)} recommendations. Analysis shows focus needed on inventory management and pricing optimization."

    def _generate_summary(self, query: str, recommendations: List[Recommendation], market_data: Dict) -> str:
        """Generate a natural language summary of recommendations."""
        if not self.llm or not recommendations:
            return f"Generated {len(recommendations)} recommendations based on current market analysis."
        
        try:
            rec_text = self.engine.format_recommendations_for_llm(recommendations)
            
            template = """
            You are a business consultant for Ethiopian marketplace sellers. 
            
            User asked: "{query}"
            
            Based on market analysis, here are the key recommendations:
            {recommendations}
            
            Market snapshot: {market_data}
            
            CRITICAL FORMATTING RULES:
            - Write in plain text ONLY like you're having a friendly conversation with a colleague
            - NEVER use asterisks (*), bold text (**), bullet points, numbered lists, or any markdown formatting
            - Instead of bullet points, use natural transitions like "First," "Also," "Additionally," "Finally"
            - Write in a warm, conversational tone as if speaking directly to the person
            
            Provide a clear, actionable summary that:
            - Directly addresses the user's question
            - Highlights the most important recommendations  
            - Considers Ethiopian market context and seasonal factors
            - Keeps a professional but warm, human tone
            
            Summary:"""
            
            prompt = PromptTemplate(template=template, input_variables=["query", "recommendations", "market_data"])
            chain = prompt | self.llm
            
            result = chain.invoke({
                "query": query,
                "recommendations": rec_text,
                "market_data": str(market_data)
            })
            
            return result.content
            
        except Exception as e:
            error_message = str(e).lower()
            
            if "resource_exhausted" in error_message or "quota" in error_message or "429" in error_message:
                return f"Recommendation Engine experienced a technical hurdle. Generated {len(recommendations)} recommendations but AI summary is temporarily unavailable due to high system demand."
            else:
                return f"Generated {len(recommendations)} recommendations. Analysis shows focus needed on inventory management and pricing optimization."

    def _add_ethiopian_context(self, recommendations: List[Recommendation]) -> str:
        """Add Ethiopian market context to recommendations."""
        context_items = []
        
        for rec in recommendations:
            if rec.type == RecommendationType.PRICING:
                context_items.append("Consider Ethiopian holiday seasons (Meskel, Timkat, Fasika) for pricing adjustments")
            elif rec.type == RecommendationType.INVENTORY:
                context_items.append("Account for Meher and Belg harvest seasons when planning inventory")
            elif rec.type == RecommendationType.DEMAND_FORECAST:
                context_items.append("Ethiopian fasting periods may affect demand for certain product categories")
        
        return "; ".join(set(context_items)) if context_items else "Consider local Ethiopian market dynamics and seasonal patterns"
    