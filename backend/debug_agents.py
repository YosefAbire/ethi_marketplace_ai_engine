#!/usr/bin/env python3
"""
Debug script to identify specific agent issues.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from api.main import seller_agent, ops_agent

def debug_seller_agent():
    print("=== Debugging Seller Agent ===")
    try:
        result = seller_agent.get_advice("How can I improve my sales?", data_context="Test context")
        print(f"Full response: {result}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def debug_ops_agent():
    print("\n=== Debugging Operations Agent ===")
    try:
        result = ops_agent.manage_ops("What's the status of recent orders?")
        print(f"Full response: {result}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_seller_agent()
    debug_ops_agent()