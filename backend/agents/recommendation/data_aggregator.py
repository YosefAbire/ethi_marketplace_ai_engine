"""
Data Aggregation Layer for Recommendation Engine
Fetches and preprocesses marketplace data via SQL Agent
"""

import pandas as pd
from typing import List, Dict


class DataAggregator:
    """
    Fetches and preprocesses marketplace data via SQL Agent.
   Converts SQL Agent string responses into structured Python objects.
    """
    
    def __init__(self, sql_agent):
        self.sql_agent = sql_agent
    
    def get_transaction_history(self, product_id: int, days: int = 90) -> pd.DataFrame:
        """
        Fetches order history for a product.
        
        Returns:
            DataFrame with columns: date, quantity, amount, buyer_id
        """
        query = f"""
        SELECT date, quantity, amount, buyer_id 
        FROM orders 
        WHERE product_id = {product_id} 
        AND status = 'completed'
        AND date >= NOW() - INTERVAL '{days} days'
        ORDER BY date
        """
        
        try:
            # Execute query using sql_agent's engine
            result = self.sql_agent.engine.execute(query)
            rows = result.fetchall()
            
            if not rows:
                return pd.DataFrame(columns=['date', 'quantity', 'amount', 'buyer_id'])
            
            df = pd.DataFrame(rows, columns=['date', 'quantity', 'amount', 'buyer_id'])
            df['date'] = pd.to_datetime(df['date'])
            return df
        except Exception as e:
            print(f"Error fetching transaction history for product {product_id}: {e}")
            return pd.DataFrame(columns=['date', 'quantity', 'amount', 'buyer_id'])
    
    def get_seller_products(self, seller_id: str) -> List[Dict]:
        """
        Retrieves all products for a specific seller.
        
        Returns:
            List of dicts: [{"id": int, "name": str, "price": float, "stock": int, "category": str}, ...]
        """
        query = f"""
        SELECT id, name, price, stock, category 
        FROM products 
        WHERE seller = '{seller_id}'
        """
        
        try:
            result = self.sql_agent.engine.execute(query)
            products = []
            for row in result:
                products.append({
                    "id": row[0],
                    "name": row[1],
                    "price": float(row[2]),
                    "stock": int(row[3]),
                    "category": row[4] if len(row) > 4 else "Uncategorized"
                })
            return products
        except Exception as e:
            print(f"Error fetching seller products for {seller_id}: {e}")
            return []
    
    def get_market_metrics(self, category: str = None) -> Dict:
        """
        Fetches marketplace-wide or category-specific metrics.
        
        Returns:
            {"avg_price": float, "avg_sales_volume": float}
        """
        if category:
            query = f"""
            SELECT AVG(price) as avg_price, COUNT(*) as product_count
            FROM products 
            WHERE category = '{category}'
            """
        else:
            query = """
            SELECT AVG(price) as avg_price, COUNT(*) as product_count
            FROM products
            """
        
        try:
            result = self.sql_agent.engine.execute(query)
            row = result.fetchone()
            return {
                "avg_price": float(row[0]) if row and row[0] else 0.0,
                "product_count": int(row[1]) if row and len(row) > 1 else 0
            }
        except Exception as e:
            print(f"Error fetching market metrics: {e}")
            return {"avg_price": 0.0, "product_count": 0}
    
    def get_product_details(self, product_id: int) -> Dict:
        """Fetches detailed product information"""
        query = f"""
        SELECT id, name, price, stock, category, seller, rating 
        FROM products 
        WHERE id = {product_id}
        """
        
        try:
            result = self.sql_agent.engine.execute(query)
            row = result.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "price": float(row[2]),
                    "stock": int(row[3]),
                    "category": row[4],
                    "seller": row[5],
                    "rating": float(row[6]) if len(row) > 6 and row[6] else 0.0
                }
        except Exception as e:
            print(f"Error fetching product details for {product_id}: {e}")
        
        return {}
