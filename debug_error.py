#!/usr/bin/env python
"""
🔴 CRITICAL DEBUG SCRIPT - For when "Server error occurred" appears
Run this to identify the EXACT problem
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(name, method, url, data=None):
    """Test an endpoint and return detailed info"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {name}")
    print(f"   URL: {method} {url}")
    if data:
        print(f"   Data: {json.dumps(data, indent=10)}")
    
    try:
        if method == 'GET':
            response = requests.get(url, timeout=15)
        else:
            response = requests.post(url, json=data, timeout=15)
        
        print(f"   Status: {response.status_code}")
        
        try:
            json_resp = response.json()
            print(f"   ✅ Response JSON:")
            print(f"   {json.dumps(json_resp, indent=6)}")
            
            if response.status_code != 200:
                print(f"   ❌ ERROR FOUND: {json_resp}")
                return False
            return True
        except:
            print(f"   📝 Response Text: {response.text[:300]}")
            return response.status_code == 200
            
    except requests.exceptions.Timeout:
        print(f"   ❌ TIMEOUT - Server is not responding fast enough")
        return False
    except requests.exceptions.ConnectionError:
        print(f"   ❌ CONNECTION ERROR - Server is not running")
        return False
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("🔴 SENTINEL AI - SERVER ERROR DEBUGGER")
    print("="*60)
    
    # Step 1: Check if servers are running
    print("\n📋 STEP 1: Check if servers are running...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/test-api", timeout=3)
        print("   ✅ Main server (5000) is running")
    except:
        print("   ❌ Main server NOT running!")
        print("      Run in Terminal: python app.py")
        return
    
    # Step 2: Test database
    print("\n📋 STEP 2: Testing database...")
    if not test_endpoint("Database Test", "GET", f"{BASE_URL}/api/test-db"):
        print("   ⚠️  Database test failed - this might be the issue!")
    
    # Step 3: Test simplified chat
    print("\n📋 STEP 3: Testing simplified chat (no auth)...")
    if not test_endpoint("Simplified Chat", "POST", f"{BASE_URL}/api/test-simple", 
                        {"message": "Hello, what is 2+2?"}):
        print("   ⚠️  Simplified chat failed!")
    
    # Step 4: Test API connection
    print("\n📋 STEP 4: Testing GROQ API connection...")
    test_endpoint("GROQ API Test", "GET", f"{BASE_URL}/api/test-api?msg=Hello")
    
    # Step 5: Recommendations
    print("\n" + "="*60)
    print("💡 RECOMMENDATIONS")
    print("="*60)
    
    print("""
1. Check Terminal Output:
   - Look for any error messages when starting the server
   - Copy the full error and search for it

2. Check Browser Console:
   - Press F12 → Console
   - Look for error messages
   - Copy them here

3. Common issues:
   - API Key invalid/expired → Update in app.py line 28
   - Database locked → Delete sentinel_ai_full.db and restart
   - Port in use → Change port in app.py
   - Missing dependencies → pip install -r requirements.txt

4. If still stuck:
   - Run: python diagnose.py
   - Check: TROUBLESHOOTING.md for detailed guide
""")
    
    print("\n" + "="*60)
    print("✨ Debug test complete!")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAborted by user")
        sys.exit(1)
