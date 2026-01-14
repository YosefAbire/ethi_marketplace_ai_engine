MARKETPLACE_SCHEMA = """
Tables:

users(id, name, role)
sellers(id, user_id, store_name)
products(id, seller_id, name, price, stock)
orders(id, user_id, created_at, total_amount)
order_items(id, order_id, product_id, quantity, price)
"""
