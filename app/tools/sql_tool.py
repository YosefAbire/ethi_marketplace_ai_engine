from app.db.postgres import execute_sql
from app.security import validate_sql

def run_safe_sql(sql: str):
    validate_sql(sql)
    return execute_sql(sql)
