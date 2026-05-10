#!/usr/bin/env python
"""
Minimal reproduction of the chat error
Run this to see what's causing "Server error occurred"
"""

import sys
import os
sys.path.insert(0, os.getcwd())

# Test 1: Import check
print("\n1️⃣  Checking imports...")
try:
    from flask import Flask, jsonify, request
    from sqlalchemy import create_engine
    from datetime import datetime, timedelta
    import jwt, uuid
    print("   ✅ All imports successful")
except Exception as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Database check
print("\n2️⃣  Checking database...")
try:
    from app import engine, Session, ChatMessage, ChatSession, User, LoginLog
    db = Session()
    count = db.query(User).count()
    print(f"   ✅ Database OK - {count} users found")
    db.close()
except Exception as e:
    print(f"   ❌ Database error: {e}")
    sys.exit(1)

# Test 3: Create test session and message
print("\n3️⃣  Testing chat endpoint logic...")
try:
    db = Session()
    
    # Create test user
    test_user_id = str(uuid.uuid4())
    test_user = User(
        id=test_user_id,
        email=f"test_{int(datetime.now().timestamp())}@test.com",
        name="Test User"
    )
    db.add(test_user)
    db.commit()
    print(f"   ✅ Created test user: {test_user_id}")
    
    # Create test session
    session_id = str(uuid.uuid4())
    test_session = ChatSession(
        id=session_id,
        user_id=test_user_id,
        title="Test - hello"
    )
    db.add(test_session)
    db.commit()
    print(f"   ✅ Created test session: {session_id}")
    
    # Create test message
    test_msg = ChatMessage(
        session_id=session_id,
        user_email=test_user.email,
        role='user',
        content="hello",
        security_label="SAFE"
    )
    db.add(test_msg)
    db.commit()
    print(f"   ✅ Created test message")
    
    # Retrieve it
    retrieved = db.query(ChatMessage).filter_by(session_id=session_id).first()
    print(f"   ✅ Retrieved message: {retrieved.content if retrieved else 'NOT FOUND'}")
    
    # Create AI response
    ai_msg = ChatMessage(
        session_id=session_id,
        user_email=test_user.email,
        role='assistant',
        content="This is a test response",
        security_label="SAFE"
    )
    db.add(ai_msg)
    db.commit()
    print(f"   ✅ Created AI response")
    
    # Count messages
    msg_count = db.query(ChatMessage).filter_by(session_id=session_id).count()
    print(f"   ✅ Total messages in session: {msg_count}")
    
    db.close()
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: API test
print("\n4️⃣  Testing GROQ API connection...")
try:
    from app import MY_API_KEY
    import requests
    
    if not MY_API_KEY or len(MY_API_KEY) < 10:
        print(f"   ❌ API Key invalid: {MY_API_KEY}")
        sys.exit(1)
    
    print(f"   ✅ API Key found")
    
    # Make test API call
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    print(f"   📊 API Response Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if 'choices' in data and len(data['choices']) > 0:
            reply = data['choices'][0]['message']['content']
            print(f"   ✅ Got response: {reply[:50]}...")
        else:
            print(f"   ❌ No choices in response: {data}")
    else:
        print(f"   ❌ API Error: {response.status_code}")
        print(f"      {response.text[:200]}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("✨ All checks complete!")
print("="*70 + "\n")
