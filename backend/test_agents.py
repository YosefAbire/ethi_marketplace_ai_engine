#!/usr/bin/env python3
"""
Simple test script to verify all agents are working properly.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from api.main import (
    sql_agent, workflow_agent, rag_agent, 
    seller_agent, ops_agent, recommendation_agent
)

def test_sql_agent():
    print("Testing SQL Agent...")
    try:
        query = "show me all products"
        sql_query = sql_agent.query_inventory(query)
        print(f"✓ SQL Agent generated query: {sql_query[:50]}...")
        return True
    except Exception as e:
        print(f"✗ SQL Agent failed: {e}")
        return False

def test_workflow_agent():
    print("Testing Workflow Agent...")
    try:
        if workflow_agent:
            route = workflow_agent.route_query("show me inventory")
            print(f"✓ Workflow Agent routed to: {route}")
            return True
        else:
            print("✗ Workflow Agent not initialized")
            return False
    except Exception as e:
        print(f"✗ Workflow Agent failed: {e}")
        return False

def test_rag_agent():
    print("Testing RAG Agent...")
    try:
        if rag_agent:
            result = rag_agent.ask("What is the marketplace about?")
            print(f"✓ RAG Agent responded: {result['answer'][:50]}...")
            return True
        else:
            print("✗ RAG Agent not initialized")
            return False
    except Exception as e:
        print(f"✗ RAG Agent failed: {e}")
        return False

def test_seller_agent():
    print("Testing Seller Agent...")
    try:
        if seller_agent:
            result = seller_agent.get_advice("How can I improve my sales?")
            print(f"✓ Seller Agent responded: {result['answer'][:50]}...")
            return True
        else:
            print("✗ Seller Agent not initialized")
            return False
    except Exception as e:
        print(f"✗ Seller Agent failed: {e}")
        return False

def test_ops_agent():
    print("Testing Operations Agent...")
    try:
        if ops_agent:
            result = ops_agent.manage_ops("What's the status of recent orders?")
            print(f"✓ Operations Agent responded: {result['answer'][:50]}...")
            return True
        else:
            print("✗ Operations Agent not initialized")
            return False
    except Exception as e:
        print(f"✗ Operations Agent failed: {e}")
        return False

def test_recommendation_agent():
    print("Testing Recommendation Agent...")
    try:
        if recommendation_agent:
            result = recommendation_agent.generate_recommendations("What should I restock?")
            print(f"✓ Recommendation Agent responded: {result['summary'][:50]}...")
            return True
        else:
            print("✗ Recommendation Agent not initialized")
            return False
    except Exception as e:
        print(f"✗ Recommendation Agent failed: {e}")
        return False

def main():
    print("=== AI Agents Test Suite ===\n")
    
    tests = [
        test_sql_agent,
        test_workflow_agent,
        test_rag_agent,
        test_seller_agent,
        test_ops_agent,
        test_recommendation_agent
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"=== Results: {passed}/{total} agents working ===")
    
    if passed == total:
        print("🎉 All agents are responding correctly!")
    else:
        print("⚠️  Some agents need attention.")

if __name__ == "__main__":
    main()