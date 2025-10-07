#!/usr/bin/env python3
"""
Test script for Trading Recommendations API
Tests all endpoints to ensure they work correctly
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_endpoint(name, url, expected_status=200):
    """Test a single endpoint"""
    try:
        response = requests.get(url, timeout=5)
        status = "✓" if response.status_code == expected_status else "✗"
        print(f"{status} {name}: Status {response.status_code}")
        if response.status_code == expected_status:
            print(f"  Response: {json.dumps(response.json(), indent=2)[:200]}...")
            return True
        else:
            print(f"  Expected {expected_status}, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ {name}: Error - {str(e)}")
        return False

def main():
    """Run all tests"""
    print("Testing Trading Recommendations API")
    print("=" * 50)
    
    tests = [
        ("Home endpoint", f"{BASE_URL}/"),
        ("Health check", f"{BASE_URL}/health"),
        ("All recommendations", f"{BASE_URL}/api/recommendations"),
        ("Specific recommendation", f"{BASE_URL}/api/recommendations/1"),
        ("Invalid recommendation", f"{BASE_URL}/api/recommendations/999", 404),
    ]
    
    results = []
    for test in tests:
        if len(test) == 2:
            name, url = test
            result = test_endpoint(name, url)
        else:
            name, url, status = test
            result = test_endpoint(name, url, status)
        results.append(result)
        print()
    
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
