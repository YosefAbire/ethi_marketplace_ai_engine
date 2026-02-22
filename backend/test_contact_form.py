#!/usr/bin/env python3
"""
Test script for the contact form API endpoint.
"""

import requests
import json

def test_contact_form():
    """Test the contact form endpoint with sample data."""
    
    # Test data
    test_data = {
        "name": "Test User",
        "email": "test@example.com",
        "company": "Test Company",
        "subject": "Test Contact Form",
        "message": "This is a test message from the contact form API test script.",
        "projectType": "consultation"
    }
    
    # API endpoint
    url = "http://localhost:8000/api/contact"
    
    try:
        print("Testing contact form API endpoint...")
        print(f"URL: {url}")
        print(f"Data: {json.dumps(test_data, indent=2)}")
        print("-" * 50)
        
        # Send POST request
        response = requests.post(
            url,
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Contact form test PASSED")
        else:
            print("❌ Contact form test FAILED")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the backend server is running:")
        print("   cd backend && python -m uvicorn api.main:app --reload")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

def test_validation():
    """Test form validation with invalid data."""
    
    print("\n" + "="*50)
    print("Testing form validation...")
    
    # Test cases for validation
    test_cases = [
        {
            "name": "Missing Name",
            "data": {
                "name": "",
                "email": "test@example.com",
                "subject": "Test",
                "message": "Test message",
                "projectType": "consultation"
            }
        },
        {
            "name": "Missing Email",
            "data": {
                "name": "Test User",
                "email": "",
                "subject": "Test",
                "message": "Test message",
                "projectType": "consultation"
            }
        },
        {
            "name": "Missing Subject",
            "data": {
                "name": "Test User",
                "email": "test@example.com",
                "subject": "",
                "message": "Test message",
                "projectType": "consultation"
            }
        },
        {
            "name": "Missing Message",
            "data": {
                "name": "Test User",
                "email": "test@example.com",
                "subject": "Test",
                "message": "",
                "projectType": "consultation"
            }
        }
    ]
    
    url = "http://localhost:8000/api/contact"
    
    for test_case in test_cases:
        try:
            print(f"\nTesting: {test_case['name']}")
            response = requests.post(url, json=test_case['data'])
            
            if response.status_code == 400:
                print(f"✅ Validation working: {response.json().get('detail')}")
            else:
                print(f"❌ Expected 400, got {response.status_code}")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_contact_form()
    test_validation()