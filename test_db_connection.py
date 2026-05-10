#!/usr/bin/env python
"""Test script to verify database connection and data persistence"""

from sqlalchemy import create_engine, text
import pandas as pd

# Test database connection
DATABASE_URL = 'sqlite:///sentinel_ai_full.db'
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False, 'timeout': 15})

try:
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = result.fetchall()
        print("✅ Database Connected!")
        print(f"📋 Tables found: {[t[0] for t in tables]}")
    
    # Check users
    users_df = pd.read_sql_query("SELECT COUNT(*) as count FROM users", engine)
    print(f"👥 Total Users: {users_df['count'].values[0]}")
    
    # Check sessions
    sessions_df = pd.read_sql_query("SELECT COUNT(*) as count FROM chat_sessions", engine)
    print(f"💬 Total Sessions: {sessions_df['count'].values[0]}")
    
    # Check messages
    messages_df = pd.read_sql_query("SELECT COUNT(*) as count FROM chat_messages", engine)
    print(f"📝 Total Messages: {messages_df['count'].values[0]}")
    
    # Check login logs
    login_df = pd.read_sql_query("SELECT COUNT(*) as count FROM login_logs", engine)
    print(f"🔐 Total Login Records: {login_df['count'].values[0]}")
    
    # Sample data
    print("\n📊 Recent Messages (Last 5):")
    sample_msgs = pd.read_sql_query("""
        SELECT user_email, role, content, created_at FROM chat_messages 
        ORDER BY created_at DESC LIMIT 5
    """, engine)
    if not sample_msgs.empty:
        print(sample_msgs.to_string())
    else:
        print("No messages yet.")
    
    print("\n✨ Database is healthy!")
    
except Exception as e:
    print(f"❌ Error: {e}")
