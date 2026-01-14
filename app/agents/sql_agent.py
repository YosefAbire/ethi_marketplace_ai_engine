from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

from app.core.config import DATABASE_URL, GOOGLE_API_KEY


def get_sql_agent():
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash",  
        temperature=0,
        api_key=GOOGLE_API_KEY
    )

    db = SQLDatabase.from_uri(
        DATABASE_URL,
        include_tables=["sellers", "products", "orders"],
        sample_rows_in_table_info=2
    )

    agent = create_sql_agent(
        llm=llm,
        db=db,
        verbose=True
    )

    return agent
