"""
Inventory Optimizer - Generates actionable inventory recommendations
"""

from typing import Dict


class InventoryOptimizer:
    """
    Generates actionable inventory recommendations.
    """
    
    def optimize(self, product_data: Dict, demand_forecast: Dict) -> Dict:
        """
        Determines optimal inventory action.
        
        Returns:
            {
                "action": str (RESTOCK/REDUCE/DISCONTINUE/MAINTAIN),
                "current_stock": int,
                "suggested_quantity": int,
                "days_of_inventory": float,
                "rationale": str,
                "impact": str (HIGH/MEDIUM/LOW)
            }
        """
        current_stock = product_data['stock']
        avg_daily_sales = demand_forecast.get('current_avg_daily_sales', 0)
        trend = demand_forecast.get('trend', 'MEDIUM')
        
        # Calculate Days of Inventory Remaining (DIR)
        dir_value = (current_stock / avg_daily_sales) if avg_daily_sales > 0 else 999
        
        # Decision logic
        if dir_value < 14 and trend in ['HIGH', 'MEDIUM']:
            action = "RESTOCK"
            # Restock to 45 days supply
            suggested_qty = max(0, int(avg_daily_sales * 45 - current_stock))
            rationale = f"Only {dir_value:.1f} days of stock remaining with {trend} demand trend. Critical restock needed."
            impact = "HIGH" if dir_value < 7 else "MEDIUM"
            
        elif dir_value > 60 and trend == 'LOW':
            action = "REDUCE"
            suggested_qty = -int(current_stock * 0.5)  # Negative indicates reduction
            rationale = f"Overstocked ({dir_value:.1f} days) with declining demand. Consider promotion to clear excess inventory."
            impact = "MEDIUM"
            
        elif avg_daily_sales == 0 and current_stock > 0:
            action = "DISCONTINUE"
            suggested_qty = -current_stock
            rationale = "Zero sales in analysis period. Consider discontinuing this product or running clearance sale."
            impact = "LOW"
            
        else:
            action = "MAINTAIN"
            suggested_qty = 0
            rationale = f"Stock levels are healthy ({dir_value:.1f} days supply). No action needed."
            impact = "LOW"
        
        return {
            "action": action,
            "current_stock": current_stock,
            "suggested_quantity": suggested_qty,
            "days_of_inventory": round(dir_value, 1),
            "rationale": rationale,
            "impact": impact,
            "demand_trend": trend
        }
