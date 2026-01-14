from sqlalchemy import create_engine, text
from  app.core.config import DATABASE_URL, GOOGLE_API_KEY


engine = create_engine(DATABASE_URL, future=True)

def execute_sql(query: str):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row) for row in result]
