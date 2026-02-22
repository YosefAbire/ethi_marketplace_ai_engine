"""
Impact Scorer - Prioritizes recommendations by business impact
"""

from typing import Dict, Tuple


class ImpactScorer:
    """
    Prioritizes recommendations by business impact using a weighted scoring model.
    """
    
    def score(self, recommendation: Dict, seller_revenue: float = 10000) -> Tuple[str, float]:
        """
        Calculates impact score and priority level.
        
        Args:
            recommendation: Output from analyzer
            seller_revenue: Total monthly seller revenue for normalization (default: 10,000 ETB)
        
        Returns:
            (priority: str, score: float)
        """
        # Revenue Impact Component (40%)
        revenue_impact = abs(recommendation.get('expected_revenue_lift', 0))
        revenue_score = min(revenue_impact / seller_revenue, 1.0)
        
        # Urgency Component (30%)
        urgency_score = self._calculate_urgency(recommendation)
        
        # Confidence Component (30%)
        confidence_score = self._confidence_to_score(recommendation.get('confidence', 'Medium'))
        
        # Weighted sum
        total_score = (revenue_score * 0.4) + (urgency_score * 0.3) + (confidence_score * 0.3)
        
        # Classify priority
        if total_score > 0.7 or revenue_impact > 500:
            priority = "HIGH"
        elif total_score > 0.4:
            priority = "MEDIUM"
        else:
            priority = "LOW"
        
        return priority, round(total_score, 3)
    
    def _calculate_urgency(self, rec: Dict) -> float:
        """Maps action/inventory status to urgency score"""
        action = rec.get('action', '')
        days_inventory = rec.get('days_of_inventory', 999)
        
        if action == 'RESTOCK' and days_inventory < 7:
            return 1.0  # Critical stock-out risk
        elif action == 'RESTOCK':
            return 0.6  # Approaching threshold
        elif action == 'REDUCE':
            return 0.4  # Overstocked
        elif action == 'DISCONTINUE':
            return 0.2  # Low priority
        else:
            return 0.1  # Maintain status
    
    def _confidence_to_score(self, confidence: str) -> float:
        """Maps confidence level to numeric score"""
        mapping = {
            'High': 1.0,
            'Medium': 0.6,
            'Low': 0.3,
            'None': 0.0
        }
        return mapping.get(confidence, 0.5)
