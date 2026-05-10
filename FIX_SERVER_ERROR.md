# 🔴 "Server error occurred" - COMPLETE FIX GUIDE

## ⚡ Quick Fix (Try This First!)

### Step 1: Check If Everything Is Running
```bash
# Terminal 1 - Main App
python app.py

# Terminal 2 - Admin Server  
python admin_server.py

# Terminal 3 - Run Debug Script
python debug_error.py
```

### Step 2: What the Debug Script Will Show
```
✅ means that part is working
❌ means that part has an issue
```

---

## 🔍 Diagnostic Checklist

### Issue 1: "Server error occurred" when sending a message

**Causes:**
1. Database is corrupted or locked
2. API key is invalid
3. Session creation is failing
4. ChatMessage table has issues

**Fix:**
```bash
# Step 1: Stop all servers (Ctrl+C in terminals)

# Step 2: Delete corrupted database
del sentinel_ai_full.db

# Step 3: Delete cache files
del -r __pycache__
del *.pyc

# Step 4: Restart servers
python app.py
```

### Issue 2: Admin Panel Shows No Data (0 users, 0 breaches)

**Possible Causes:**
1. No chat messages yet - this is NORMAL if you haven't chatted
2. Admin endpoints are not working
3. Database connection issue

**Check:**
1. Send a test message first in the chat app
2. Wait 5 seconds
3. Refresh admin panel
4. Should now show data

**If Still Empty:**
```bash
# Test admin endpoints directly
http://127.0.0.1:5001/api/health
http://127.0.0.1:5001/api/users-stats  
http://127.0.0.1:5001/api/live-logs
```

---

## 🧪 Step-by-Step Testing

### Test 1: Database Connection
```bash
# Terminal 3
http://127.0.0.1:5000/api/test-db
```
Should see:
```json
{
  "success": true,
  "message": "Database test passed"
}
```

### Test 2: Simple Chat (No Auth)
```bash
http://127.0.0.1:5000/api/test-simple -POST
Body: {"message": "Hello"}
```
Should see:
```json
{
  "success": true,
  "reply": "Response from GROQ API..."
}
```

### Test 3: Admin Health Check
```bash
http://127.0.0.1:5001/api/health
```
Should see:
```json
{
  "status": "OK",
  "message": "Admin Server is running"
}
```

---

## 🐛 Common Errors & Fixes

### Error: "Internal Server Error"
**Check:**
1. Browser Console (F12 → Console tab)
2. Terminal where app.py is running - look for error message
3. Copy the error and check below

### Error: "Cannot read property 'reply' of undefined"
**Means:** Server didn't send a proper reply
**Fix:**
1. Stop app with Ctrl+C
2. Delete database: `del sentinel_ai_full.db`
3. Restart app
4. Try sending message again

### Error: "401 Unauthorized" or "Invalid token"
**Means:** Session expired
**Fix:**
1. Logout: Click power button
2. Login again with Google
3. Try sending message

### Error: "Database is locked"
**Means:** Database file is being used by multiple processes
**Fix:**
```bash
# Kill all Python processes
taskkill /F /IM python.exe

# Or restart terminals
# Then start fresh:
python app.py
```

### Error: "API Key invalid or missing"
**Fix:**
1. Open app.py
2. Go to line 28
3. Look for: `MY_API_KEY = "gsk_..."`
4. Get new key from: https://console.groq.com/keys
5. Copy and paste key
6. Restart app

---

## 📊 How to Read Debug Output

### Terminal Output While App is Running

**Good Signs:**
```
✅ Saved user message
🔄 Calling GROQ API with model: llama-3.3-70b-versatile
📊 API Response Status: 200
✅ Got response from API: 145 chars
✅ Saved AI response and updated session
```

**Bad Signs:**
```
❌ Chat Error: [error message here]
❌ API Key issue
❌ Request timeout to GROQ API
❌ Connection error
```

---

## 🚀 Final Nuclear Option (If nothing else works)

```bash
# 1. Kill all Python processes
taskkill /F /IM python.exe

# 2. Delete everything and start fresh
del sentinel_ai_full.db
del -r __pycache__
del -r .pytest_cache

# 3. Reinstall dependencies
pip install --upgrade flask flask-cors sqlalchemy pandas requests PyJWT

# 4. Start fresh
python app.py
```

---

## 📝 Files to Check

1. **app.py** - Main application
   - Line 28: Check MY_API_KEY
   - Lines 220-350: Chat endpoint logic

2. **admin_server.py** - Admin dashboard backend  
   - Lines 90-160: API endpoints

3. **templates/admin_dashboard.html** - Frontend admin
   - Look at Network tab (F12) to see requests

4. **templates/index.html** - Chat frontend
   - Console (F12) shows detailed logs

---

## 💬 Getting Help

When asking for help, provide:
1. Full error message from terminal
2. Screenshot of browser console (F12)
3. Output from: `python debug_error.py`
4. Which step you're stuck on

---

**Last Updated:** 2026-03-04  
**Created for:** Sentinel AI Debugging  
**Purpose:** Fix "Server error occurred" issues
