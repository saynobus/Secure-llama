#!/usr/bin/env python
"""Comprehensive debug script to test API and database"""

import requests
import json
from datetime import datetime

print("\n" + "="*60)
print("🔍 SENTINEL AI - FULL DEBUG TEST")
print("="*60 + "\n")

# Test 1: Database Connection
print("1️⃣  Testing Database Connection...")
try:
    response = requests.get('http://127.0.0.1:5000/api/test-db')
    result = response.json()
    if result.get('success'):
        print(f"   ✅ Database OK - {result.get('users_count')} users found")
    else:
        print(f"   ❌ Database Error: {result.get('error')}")
except Exception as e:
    print(f"   ❌ Connection Error: {e}")

# Test 2: API Connection (No Auth Required)
print("\n2️⃣  Testing GROQ API Connection...")
try:
    response = requests.get('http://127.0.0.1:5000/api/test-api?msg=What%20is%20AI%3F')
    result = response.json()
    if result.get('success'):
        print(f"   ✅ GROQ API OK")
        print(f"   📝 Response: {result.get('message')[:100]}...")
    else:
        print(f"   ❌ GROQ API Error: {result.get('error')[:200]}")
except Exception as e:
    print(f"   ❌ Connection Error: {e}")

# Test 3: Check if server is running
print("\n3️⃣  Testing Server Status...")
try:
    response = requests.get('http://127.0.0.1:5000/')
    if response.status_code == 200:
        print(f"   ✅ Flask Server Running on port 5000")
    else:
        print(f"   ⚠️  Server returned status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Server Not Running: {e}")

# Test 4: Admin Server Status
print("\n4️⃣  Testing Admin Server Status...")
try:
    response = requests.get('http://127.0.0.1:5001/')
    if response.status_code == 200:
        print(f"   ✅ Admin Server Running on port 5001")
    else:
        print(f"   ⚠️  Admin Server returned status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Admin Server Not Running: {e}")

print("\n" + "="*60)
print("✨ Debug test complete!")
print("="*60 + "\n")

print("📌 Quick Actions:")
print("   • Test API: http://127.0.0.1:5000/api/test-api")
print("   • Test DB: http://127.0.0.1:5000/api/test-db")
print("   • Admin Panel: http://127.0.0.1:5001/")
print("   • Chat App: http://127.0.0.1:5000/dashboard\n")
