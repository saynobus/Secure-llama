#!/usr/bin/env python
"""
Ultra simple starter - just run this and send a message
It will capture all errors to debug.log
"""

import os
import sys

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Clear old logs
if os.path.exists('debug.log'):
    os.remove('debug.log')

print("\n" + "="*70)
print("🚀 STARTING SENTINEL AI - WATCH FOR ERRORS BELOW")
print("="*70 + "\n")

# Run the app
print("Starting Flask app on port 5000...\n")
os.system("python app.py")
