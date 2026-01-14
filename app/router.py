from app.agents.sql_agent import sql_intelligence_agent

def route_query(query: str):
    # Later this will route to RAG / Ops / Workflow
    return sql_intelligence_agent(query)
