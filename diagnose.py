#!/usr/bin/env python
"""
🔍 Sentinel AI - Comprehensive Diagnostic Tool
Checks all critical systems and reports issues
"""

import os
import sys
import json
import requests
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_status(icon, msg, status="info"):
    color = Colors.RESET
    if status == "success":
        color = Colors.GREEN
    elif status == "error":
        color = Colors.RED
    elif status == "warning":
        color = Colors.YELLOW
    print(f"{color}{icon} {msg}{Colors.RESET}")

def check_file_exists(path, name):
    if os.path.exists(path):
        print_status("✅", f"{name} found", "success")
        return True
    else:
        print_status("❌", f"{name} NOT FOUND at {path}", "error")
        return False

def test_server(port, name):
    try:
        response = requests.get(f'http://127.0.0.1:{port}/', timeout=3)
        print_status("✅", f"{name} (:{port}) is running", "success")
        return True
    except requests.exceptions.ConnectError:
        print_status("❌", f"{name} (:{port}) is NOT running", "error")
        return False
    except Exception as e:
        print_status("⚠️", f"{name} (:{port}) error: {e}", "warning")
        return False

def test_api():
    try:
        response = requests.get('http://127.0.0.1:5000/api/test-api?msg=Testing', timeout=10)
        data = response.json()
        
        if data.get('success'):
            print_status("✅", "GROQ API is responding correctly", "success")
            return True
        else:
            error = data.get('error', 'Unknown error')
            if 'API Key' in error or 'authentication' in error.lower():
                print_status("❌", f"API Key Issue: {error[:100]}", "error")
            else:
                print_status("❌", f"GROQ API Error: {error[:100]}", "error")
            return False
            
    except requests.exceptions.Timeout:
        print_status("❌", "GROQ API timeout - check internet connection", "error")
        return False
    except Exception as e:
        print_status("❌", f"Failed to test GROQ API: {str(e)[:100]}", "error")
        return False

def test_database():
    try:
        response = requests.get('http://127.0.0.1:5000/api/test-db', timeout=5)
        data = response.json()
        
        if data.get('success'):
            users = data.get('users_count', 0)
            print_status("✅", f"Database is OK ({users} users)", "success")
            return True
        else:
            print_status("❌", f"Database Error: {data.get('error')}", "error")
            return False
            
    except Exception as e:
        print_status("❌", f"Failed to test database: {str(e)}", "error")
        return False

def check_api_key():
    try:
        # Read app.py to check API key
        with open('app.py', 'r') as f:
            content = f.read()
            if 'MY_API_KEY = ""' in content or 'MY_API_KEY = \'\'' in content:
                print_status("❌", "API Key is EMPTY in app.py (line 28)", "error")
                return False
            elif 'gsk_' in content:
                print_status("✅", "API Key appears to be set in app.py", "success")
                return True
            else:
                print_status("⚠️", "Cannot determine API Key status", "warning")
                return None
    except FileNotFoundError:
        print_status("❌", "app.py not found", "error")
        return False
    except Exception as e:
        print_status("⚠️", f"Could not check API Key: {e}", "warning")
        return None

def get_summary_report(results):
    print("\n" + "="*60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    warnings = sum(1 for v in results.values() if v is None)
    
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    if warnings > 0:
        print(f"⚠️  Warnings: {warnings}")
    
    print("\n" + "="*60)
    
    if failed == 0 and passed >= 4:
        print_status("🎉", "Everything looks good! Check browser console if messages still don't work", "success")
        return True
    elif failed <= 2:
        print_status("⚠️", "Some issues found - see recommendations below", "warning")
        return False
    else:
        print_status("❌", "Critical issues detected - fix them before using the app", "error")
        return False

def print_recommendations(results):
    print("\n" + "="*60)
    print("💡 RECOMMENDATIONS")
    print("="*60)
    
    if not results.get('servers'):
        print("1. Start the Flask server: python app.py")
        print("2. Start the admin server: python admin_server.py")
    
    if not results.get('api'):
        print("• Check your internet connection")
        print("• Verify GROQ API key in app.py (line 28)")
        print("• Visit: https://console.groq.com/keys to get a new API key")
        print("• Add API key to app.py and restart")
    
    if not results.get('database'):
        print("• Try deleting sentinel_ai_full.db and restarting")
        print("• Check file permissions in current directory")
    
    print("\n" + "="*60)

def main():
    print("\n" + "="*60)
    print("🔍 SENTINEL AI - DIAGNOSTIC TOOL")
    print("="*60 + "\n")
    
    results = {}
    
    # Check critical files
    print("📂 Checking Files...")
    check_file_exists('app.py', 'app.py')
    check_file_exists('admin_server.py', 'admin_server.py')
    check_file_exists('templates/index.html', 'Frontend files')
    
    print("\n🔌 Checking Servers...")
    results['servers'] = test_server(5000, "Main Server") and test_server(5001, "Admin Server")
    
    if not results['servers']:
        print_status("⚠️", "Servers not running - starting tests anyway...", "warning")
    
    print("\n🔐 Checking API Configuration...")
    results['api_key'] = check_api_key()
    
    print("\n🌐 Testing GROQ API Connection...")
    results['api'] = test_api()
    
    print("\n💾 Testing Database...")
    results['database'] = test_database()
    
    # Summary
    success = get_summary_report(results)
    print_recommendations(results)
    
    if success:
        print_status("✨", "Diagnostic complete - no major issues found", "success")
    else:
        print_status("🔧", "Please fix the issues above and try again", "warning")
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAborted by user")
        sys.exit(1)
    except Exception as e:
        print_status("❌", f"Unexpected error: {e}", "error")
        sys.exit(1)
