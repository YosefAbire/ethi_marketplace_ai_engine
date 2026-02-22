"""
Pricing Analyzer - Calculates optimal pricing using elasticity and market positioning
"""

import numpy as np
import pandas as pd
from typing import Dict


class PricingAnalyzer:
    """
    Calculates optimal pricing using demand elasticity and market positioning.
    """
    
    def analyze(self, product_data: Dict, transaction_history: pd.DataFrame, 
                market_metrics: Dict) -> Dict:
        """
        Main analysis method.
        
        Args:
            product_data: Current product info (price, stock, category)
            transaction_history: Historical sales data
            market_metrics: Category averages
        
        Returns:
            {
                "current_price": float,
                "recommended_price": float,
                "expected_revenue_lift": float,
                "confidence": str,
                "market_position": str,
                "rationale": str
            }
        """
        if transaction_history.empty:
            return self._insufficient_data_response(product_data)
        
        current_price = product_data['price']
        
        # Calculate price elasticity
        elasticity = self._calculate_elasticity(transaction_history)
        
        # Find optimal price
        avg_monthly_sales = len(transaction_history) / 3  # Assuming 90 days
        optimal_price = self._find_optimal_price(
            current_price=current_price,
            elasticity=elasticity,
            base_demand=avg_monthly_sales,
            category_avg=market_metrics.get('avg_price', current_price)
        )
        
        # Calculate revenue impact
        current_monthly_revenue = current_price * avg_monthly_sales
        projected_demand = avg_monthly_sales * (1 + elasticity * (optimal_price - current_price) / current_price)
        projected_revenue = optimal_price * projected_demand
        revenue_lift = projected_revenue - current_monthly_revenue
        
        # Market positioning
        category_avg = market_metrics.get('avg_price', current_price)
        if optimal_price < category_avg * 0.9:
            position = "Budget positioning"
        elif optimal_price > category_avg * 1.1:
            position = "Premium positioning"
        else:
            position = "Market-aligned"
        
        # Confidence score
        confidence = self._calculate_confidence(transaction_history)
        
        return {
            "current_price": round(current_price, 2),
            "recommended_price": round(optimal_price, 2),
            "expected_revenue_lift": round(revenue_lift, 2),
            "confidence": confidence,
            "market_position": position,
            "category_avg_price": round(category_avg, 2),
            "price_elasticity": round(elasticity, 2),
            "rationale": self._generate_rationale(
                current_price, optimal_price, elasticity, position, revenue_lift
            )
        }
    
    def _calculate_elasticity(self, df: pd.DataFrame) -> float:
        """
        Computes price elasticity: % change in quantity / % change in price
        """
        if len(df) < 10:
            return -1.2  # Default assumption for elastic goods
        
        # Calculate price per unit
        df = df.copy()
        df['unit_price'] = df['amount'] / df['quantity']
        
        # Group by price points
        price_groups = df.groupby(pd.cut(df['unit_price'], bins=min(5, len(df)//2)))['quantity'].sum()
        
        valid_groups = [(interval.mid, qty) for interval, qty in price_groups.items() if qty > 0]
        
        if len(valid_groups) < 2:
            return -1.2
        
        # Simple elasticity: compare highest and lowest price points
        valid_groups.sort()
        p1, q1 = valid_groups[0]
        p2, q2 = valid_groups[-1]
        
        if p1 == p2 or q1 == 0:
            return -1.2
        
        pct_change_qty = (q2 - q1) / q1
        pct_change_price = (p2 - p1) / p1
        
        elasticity = pct_change_qty / pct_change_price if pct_change_price != 0 else -1.2
        
        # Constrain to reasonable bounds
        return max(-5.0, min(-0.3, elasticity))
    
    def _find_optimal_price(self, current_price: float, elasticity: float, 
                           base_demand: float, category_avg: float) -> float:
        """
        Finds revenue-maximizing price using elasticity model.
        """
        # Search from 70% to 130% of current price
        price_range = np.linspace(current_price * 0.7, current_price * 1.3, 100)
        
        max_revenue = 0
        optimal_price = current_price
        
        for price in price_range:
            # Demand model: Demand(Price) = base_demand * (Price / current_price)^elasticity
            demand = base_demand * ((price / current_price) ** elasticity)
            revenue = price * demand
            
            if revenue > max_revenue:
                max_revenue = revenue
                optimal_price = price
        
        # Apply market constraints
        if optimal_price > category_avg * 1.3:
            optimal_price = category_avg * 1.2
        elif optimal_price < category_avg * 0.5:
            optimal_price = category_avg * 0.7
        
        return optimal_price
    
    def _calculate_confidence(self, df: pd.DataFrame) -> str:
        """Confidence based on data sufficiency"""
        data_points = len(df)
        if data_points >= 60:
            return "High"
        elif data_points >= 30:
            return "Medium"
        else:
            return "Low"
    
    def _generate_rationale(self, current: float, recommended: float, 
                           elasticity: float, position: str, lift: float) -> str:
        """Generates human-readable explanation"""
        change_pct = ((recommended - current) / current) * 100 if current > 0 else 0
        direction = "increase" if recommended > current else "decrease" if recommended < current else "maintain"
        
        if direction == "maintain":
            return f"Current price of {current:.2f} ETB is optimal based on market analysis."
        
        return (f"Based on price elasticity of {elasticity:.2f}, a {direction} to "
                f"{recommended:.2f} ETB ({change_pct:+.1f}%) is recommended. "
                f"This maintains {position.lower()} and projects {lift:+.2f} ETB "
                f"monthly revenue impact.")
    
    def _insufficient_data_response(self, product_data: Dict) -> Dict:
        """Fallback when no transaction history available"""
        return {
            "current_price": product_data['price'],
            "recommended_price": product_data['price'],
            "expected_revenue_lift": 0.0,
            "confidence": "Low",
            "market_position": "Unknown",
            "category_avg_price": product_data['price'],
            "price_elasticity": -1.2,
            "rationale": "Insufficient sales history for pricing analysis. Maintain current price and monitor sales data."
        }
