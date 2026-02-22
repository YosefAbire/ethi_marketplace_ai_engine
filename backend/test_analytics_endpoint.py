#!/usr/bin/env python3
"""
Quick test script to verify the analytics endpoint is working.
"""

import requests
import json

def test_analytics_endpoint():
    """Test the /dashboard/analytics endpoint."""
    print("Testing /dashboard/analytics endpoint...")
    
    try:
        # Test the analytics endpoint
        response = requests.get("http://127.0.0.1:8000/dashboard/analytics")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Analytics endpoint is working!")
            print(f"   Source: {data.get('source', 'unknown')}")
            print(f"   Total customers: {data.get('total_customers', 0)}")
            print(f"   Total transactions: {data.get('total_transactions', 0)}")
            print(f"   Avg order value: {data.get('avg_order_value', 0)}")
            print(f"   Gender distribution: {len(data.get('gender_distribution', []))} categories")
            print(f"   Age distribution: {len(data.get('age_distribution', []))} groups")
            print(f"   Spending data points: {len(data.get('spending_vs_income', []))}")
            return True
        else:
            print(f"❌ Analytics endpoint failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the backend is running on port 8000.")
        return False
    except Exception as e:
        print(f"❌ Error testing analytics endpoint: {e}")
        return False

def test_other_dashboard_endpoints():
    """Test other dashboard endpoints for comparison."""
    endpoints = [
        "/dashboard/stats",
        "/dashboard/products", 
        "/dashboard/orders"
    ]
    
    print("\nTesting other dashboard endpoints...")
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://127.0.0.1:8000{endpoint}")
            if response.status_code == 200:
                print(f"✅ {endpoint} - Working")
            else:
                print(f"❌ {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")

if __name__ == "__main__":
    print("=== Analytics Endpoint Test ===\n")
    
    # Test analytics endpoint
    analytics_working = test_analytics_endpoint()
    
    # Test other endpoints
    test_other_dashboard_endpoints()
    
    print("\n" + "="*40)
    if analytics_working:
        print("🎉 Analytics endpoint is working correctly!")
        print("The 404 errors should now be resolved.")
    else:
        print("❌ Analytics endpoint needs attention.")
        print("Make sure the backend server is running.")
    print("="*40)