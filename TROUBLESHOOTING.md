# 🔧 Sentinel AI - Troubleshooting Guide

## ❌ Message Responses Not Coming? Follow These Steps:

### Step 1: Check If Servers Are Running
```bash
# In Terminal 1: Start main Flask app
python app.py

# In Terminal 2: Start admin server  
python admin_server.py

# In Terminal 3: Run debug tests
python debug_test.py
```

### Step 2: Test API Connection
Open in browser: `http://127.0.0.1:5000/api/test-api`

**Expected Response:**
```json
{
  "success": true,
  "message": "Response from GROQ API...",
  "status_code": 200
}
```

**If you see error:** API key is invalid or expired

### Step 3: Check Browser Console
Press `F12` → Click Console tab
Send a message and look for logs:
- `📤 Sending message...` - Message sent successfully
- `📥 Response Status: 200` - Server responded
- `✅ Got response:` - Response received
- `❌ Error:` - Something went wrong

### Step 4: Common Issues & Fixes

#### 🔴 Issue: "Cannot find module 'requests'"
```bash
pip install requests
```

#### 🔴 Issue: "API Key missing or invalid"
1. Open `app.py` line 28
2. Check `MY_API_KEY` - should start with `gsk_`
3. If empty, visit: https://console.groq.com/keys
4. Copy your API key and paste in line 28

#### 🔴 Issue: "Database error"
The database should auto-create. To reset:
```bash
# Delete old database
del sentinel_ai_full.db

# Restart app - it will create new database
python app.py
```

#### 🔴 Issue: "Port already in use"
Either close other process or change port:
```bash
# Use different port (change 5000 to 5001, etc)
python app.py --port 5001
```

### Step 5: Check Logs Carefully

Look for these patterns in terminal output:

✅ **Good Signs:**
- `✅ Saved user message`
- `🔄 Calling GROQ API with model: llama-3.3-70b-versatile`
- `✅ Got response from API:...`
- `✅ Saved AI response and updated session`

❌ **Red Flags:**
- `❌ API Key issue`
- `❌ API Error: 401` (Invalid API key)
- `❌ API Error: 429` (Rate limited)
- `❌ Request timeout to GROQ API`
- `❌ Connection error`

### Step 6: Test Directly via Browser

1. **Test API endpoint:**
   ```
   http://127.0.0.1:5000/api/test-api?msg=Hello
   ```

2. **Test Database:**
   ```
   http://127.0.0.1:5000/api/test-db
   ```

3. **Admin Panel:**
   ```
   http://127.0.0.1:5001/
   ```

### Step 7: Enable Console Logging

Add this to browser console to see real-time logs:
```javascript
// Paste in browser console (F12)
localStorage.setItem('debug_mode', 'true');
location.reload();
```

## 📊 Quick Debug Checklist

- [ ] Both servers running (5000 + 5001)
- [ ] No errors in terminal when starting app.py
- [ ] Browser console shows no errors
- [ ] Can access: http://127.0.0.1:5000/api/test-api
- [ ] Can access: http://127.0.0.1:5000/api/test-db
- [ ] API key is set in line 28 of app.py
- [ ] Can login to Sentinel AI
- [ ] Can send a message
- [ ] See `✅ Got response from API:` in terminal

## 🚀 If Still Not Working

1. Check file: [app.py](app.py#L220-L320) - chat function
2. Look for logs with `Chat Error:` in terminal
3. Check browser Network tab (F12 → Network) for failed requests
4. Share the error message from terminal

---

**Created:** 2026-03-04
**Purpose:** Fix message response issues in Sentinel AI
