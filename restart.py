#!/usr/bin/env python
"""Quick start script to restart everything fresh"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd):
    """Run a command and show output"""
    print(f"\n▶️ {cmd}")
    result = os.system(cmd)
    return result == 0

def main():
    print("\n" + "="*70)
    print("🚀 SENTINEL AI - QUICK RESTART SCRIPT")
    print("="*70)
    
    # Step 1: Kill existing Python processes
    print("\n1️⃣  Stopping all Python processes...")
    os.system("taskkill /F /IM python.exe 2>nul")
    print("   ✅ Done")
    
    # Step 2: Check if database needs reset
    db_path = "sentinel_ai_full.db"
    if Path(db_path).exists():
        print(f"\n2️⃣  Found existing database: {db_path}")
        response = input("   Delete and start fresh? (y/n): ").strip().lower()
        if response == 'y':
            os.remove(db_path)
            print("   ✅ Database deleted")
        else:
            print("   ⏭️  Keeping existing database")
    else:
        print(f"\n2️⃣  No database found - will create new one")
    
    # Step 3: Show startup instructions
    print("\n" + "="*70)
    print("📋 STARTUP INSTRUCTIONS")
    print("="*70)
    
    print("""
    
    Open 3 separate terminals:
    
    TERMINAL 1 (Main App):
    python app.py
    
    TERMINAL 2 (Admin Server):
    python admin_server.py
    
    TERMINAL 3 (Debug/Testing):
    python debug_error.py
    
    Then:
    1. Open http://127.0.0.1:5000/login in browser
    2. Login with Google
    3. Try sending a message
    4. Check http://127.0.0.1:5001 for admin panel
    5. Run debug_error.py if it doesn't work
    """)
    
    print("\n" + "="*70)
    print("✨ Ready to start! Open the terminals above.")
    print("="*70 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled")
        sys.exit(1)
