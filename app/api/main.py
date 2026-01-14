from fastapi import FastAPI
from app.agents.sql_agent import get_sql_agent



app = FastAPI(title="Marketplace AI Agents")

sql_agent = get_sql_agent()


@app.get("/")
def health():
    return {"status": "SQL Intelligence Agent running"}


@app.post("/ask")
def ask_sql_agent(question: str):
    response = sql_agent.invoke(question)
    return {"answer": response}
