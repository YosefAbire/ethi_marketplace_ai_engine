import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

class SQLAgent:
    """
    Expert Data Analyst that translates natural language to SQL and summarizes data findings.
    """
    def __init__(self, db_engine, api_key: Optional[str] = None):
        self.engine = db_engine
        self.api_key = api_key or os.getenv("API_KEY")
        
        # Initialize LLM for SQL generation and explanation
        if self.api_key:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=self.api_key,
                temperature=0.1
            )
        else:
            self.llm = None

        # Schema definition for the LLM to understand the database
        self.schema = """
        TABLE products (id INTEGER, name TEXT, price FLOAT, stock INTEGER, category TEXT, seller TEXT, rating FLOAT)
        TABLE orders (id TEXT, product TEXT, amount FLOAT, status TEXT, date TEXT)
        """

    def query_inventory(self, prompt: str) -> str:
        """Generates a SQL query from natural language with schema context."""
        if not self.llm:
            return f"SELECT * FROM products WHERE name LIKE '%{prompt}%'"

        sql_gen_template = f"""
        You are a SQL Expert for the Ethi Marketplace. Given the following schema, write a valid SQL query to answer the user's question.
        
        SCHEMA:
        {self.schema}

        OUTPUT RULE:
        Return ONLY the SQL code block. No explanation.

        User Question: {{prompt}}
        SQL Query:"""

        prompt_template = PromptTemplate(template=sql_gen_template, input_variables=["prompt"])
        chain = prompt_template | self.llm
        
        try:
            result = chain.invoke({"prompt": prompt})
            return result.content.strip().replace('```sql', '').replace('```', '').strip()
        except Exception as e:
            error_message = str(e).lower()
            
            if "resource_exhausted" in error_message or "quota" in error_message or "429" in error_message:
                # Return a basic fallback query when AI is unavailable
                return f"SELECT * FROM products WHERE name LIKE '%{prompt}%' OR category LIKE '%{prompt}%'"
            else:
                return f"SELECT * FROM products WHERE name LIKE '%{prompt}%'"

    def summarize_results(self, data: str, query: str) -> str:
        """Explains database results in a warm, human, plain-text way."""
        if not self.llm:
            return f"I found the following data for you: {data}"

        summary_template = """
        You are a friendly Data Analyst. You just ran a query: "{query}"
        The database returned this result: {data}

        STRICT RULE: Explain these results in a natural, human way using plain text ONLY. 
        Do not use asterisks, bolding, or markdown tables. Talk like a helpful colleague.
        
        Response:"""

        prompt_template = PromptTemplate(template=summary_template, input_variables=["query", "data"])
        chain = prompt_template | self.llm
        
        try:
            result = chain.invoke({"query": query, "data": data})
            return result.content
        except Exception as e:
            error_message = str(e).lower()
            
            if "resource_exhausted" in error_message or "quota" in error_message or "429" in error_message:
                return f"SQL Agent experienced a technical hurdle. Here's your data: {data}. AI summary is temporarily unavailable due to high system demand."
            else:
                return f"Here's your requested data: {data}"
