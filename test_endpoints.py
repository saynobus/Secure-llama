#!/usr/bin/env python
import requests

print("\n📊 Testing Flask Server Endpoints\n")

# Test 1: test-quick
try:
    r = requests.get('http://127.0.0.1:5000/api/test-quick', timeout=3)
    print(f"✅ /api/test-quick: {r.status_code} - {r.json()}")
except Exception as e:
    print(f"❌ /api/test-quick failed: {e}")

# Test 2: test-api
try:
    r = requests.get('http://127.0.0.1:5000/api/test-api?msg=hello', timeout=5)
    print(f"✅ /api/test-api: {r.status_code}")
except Exception as e:
    print(f"❌ /api/test-api failed: {e}")

# Test 3: debug-log
try:
    r = requests.get('http://127.0.0.1:5000/api/debug-log', timeout=3)
    print(f"✅ /api/debug-log: {r.status_code}")
    if r.status_code == 200:
        data = r.json().get('logs', '')
        if data:
            print(f"\nDEBUG LOG:\n{data[-1000:]}")
        else:
            print("   (no logs yet)")
except Exception as e:
    print(f"❌ /api/debug-log failed: {e}")

print("\n✨ Test complete\n")
