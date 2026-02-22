#!/usr/bin/env python3
"""
Test script to check if agents are responding in a humanized way without formatting.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from api.main import (
    sql_agent, workflow_agent, rag_agent, 
    seller_agent, ops_agent, recommendation_agent,
    get_market_snapshot
)

def test_humanized_responses():
    print("=== Testing Humanized Agent Responses ===\n")
    
    # Test SQL Agent
    print("1. SQL Agent Response:")
    try:
        query = "show me products with low stock"
        sql_query = sql_agent.query_inventory(query)
        # Execute the query to get results for summarization
        from api.main import db_engine
        from sqlalchemy import text
        with db_engine.connect() as connection:
            result_proxy = connection.execute(text(sql_query))
            rows = [dict(row._mapping) for row in result_proxy]
            result_str = str(rows)
        
        summary = sql_agent.summarize_results(result_str, query)
        print(f"Response: {summary}")
        print(f"Contains asterisks: {'*' in summary}")
        print(f"Contains markdown: {'**' in summary or '##' in summary}")
        print()
    except Exception as e:
        print(f"Error: {e}\n")
    
    # Test Seller Agent
    print("2. Seller Agent Response:")
    try:
        context = get_market_snapshot()
        result = seller_agent.get_advice("How can I improve my honey sales during Ethiopian holidays?", data_context=context)
        response = result['answer']
        print(f"Response: {response[:200]}...")
        print(f"Contains asterisks: {'*' in response}")
        print(f"Contains markdown: {'**' in response or '##' in response}")
        print()
    except Exception as e:
        print(f"Error: {e}\n")
    
    # Test Operations Agent
    print("3. Operations Agent Response:")
    try:
        result = ops_agent.manage_ops("How can I track my order delivery to Addis Ababa?")
        response = result['answer']
        print(f"Response: {response[:200]}...")
        print(f"Contains asterisks: {'*' in response}")
        print(f"Contains markdown: {'**' in response or '##' in response}")
        print()
    except Exception as e:
        print(f"Error: {e}\n")
    
    # Test RAG Agent
    print("4. RAG Agent Response:")
    try:
        result = rag_agent.ask("What are the marketplace policies?")
        response = result['answer']
        print(f"Response: {response[:200]}...")
        print(f"Contains asterisks: {'*' in response}")
        print(f"Contains markdown: {'**' in response or '##' in response}")
        print()
    except Exception as e:
        print(f"Error: {e}\n")
    
    # Test Recommendation Agent
    print("5. Recommendation Agent Response:")
    try:
        result = recommendation_agent.generate_recommendations("What products should I focus on for the upcoming Meskel holiday?")
        response = result['summary']
        print(f"Response: {response[:200]}...")
        print(f"Contains asterisks: {'*' in response}")
        print(f"Contains markdown: {'**' in response or '##' in response}")
        print()
    except Exception as e:
        print(f"Error: {e}\n")

if __name__ == "__main__":
    test_humanized_responses()