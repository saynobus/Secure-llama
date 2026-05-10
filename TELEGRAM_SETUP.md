# Telegram Setup Guide

## 📱 What's Fixed

1. ✅ **GROQ Model Updated** - Changed from deprecated `llama-3.2-11b-vision-preview` to `llama-3.1-70b-versatile`
2. ✅ **Telegram Alert System** - Auto-sends alerts when dangerous prompts detected
3. ✅ **UI Improvements** - Better notifications, error messages, and loading states

---

## 🔧 Telegram Setup Instructions

### Step 1: Get Your Telegram Credentials

You need two things:
- **Chat ID**: The ID of your Telegram chat (your personal ID)
- **Bot Token**: The API token for your Telegram bot

### Step 2: Edit api.txt

**File Location**: `c:\Users\Shravan Deshmukh\Music\wt assig 3\vs ai\Secure-Llama source code\api.txt`

The file currently looks like:
```
AIzaSyEXAMPLE_KEY_1

AIzaSyEXAMPLE_KEY_2

gsk_EXAMPLE_KEY_1

tele api
TELEGRAM_CHAT_ID
TELEGRAM_BOT_TOKEN
```

### What Each Line Means

Line 10: `tele api` - Marker (leave as-is)
Line 11: `TELEGRAM_CHAT_ID` - **Chat ID** (replace with YOUR Telegram Chat ID)
Line 12: `TELEGRAM_BOT_TOKEN` - **Bot Token** (replace with YOUR Bot Token)

### Step 3: Find Your Telegram Chat ID

**Option A: Using @userinfobot**
1. Open Telegram
2. Search for `@userinfobot`
3. Start the bot
4. It will show your Chat ID (Your ID: `123456789`)
5. Copy this number

**Option B: Using @getidsbot**
1. Search for `@getidsbot`
2. Start the bot
3. It shows your ID
4. Copy this number

### Step 4: Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Start a conversation
3. Send: `/newbot`
4. Follow the prompts:
   - Name: "Sentinel AI Alerts"
   - Username: Something unique like "sentinel_ai_alerts_bot"
5. BotFather will give you a **Bot Token** (something like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

---

## 📝 Example Setup

If your credentials are:
- Chat ID: `987654321`
- Bot Token: `9876543:ABCDEfghij1234567890klmnopqrst`

Then update **api.txt** lines 11-12 to:
```
tele api
987654321
9876543:ABCDEfghij1234567890klmnopqrst
```

---

## ✅ Test Your Setup

### Method 1: Test Endpoint (Easiest)
Open in browser:
```
http://127.0.0.1:5000/api/test-telegram
```

You should see JSON response showing:
- `credentials_loaded: true`
- `test_message_sent: true`

### Method 2: Send Danger Keyword
1. Go to http://127.0.0.1:5000/login
2. Login with your account
3. Send a message with danger keywords: "hack", "bypass", "sql inject", "exploit"
4. Check your Telegram - you should get an alert!

---

## 🆘 Troubleshooting

### Alert Not Sending?

**Check 1**: Verify credentials are correct
```
http://127.0.0.1:5000/api/test-telegram
```

**Check 2**: Make sure you sent a danger keyword. Valid triggers:
- "hack"
- "bypass"  
- "exploit"
- "sql inject"
- "proxy"
- "admin access"
- "root"
- "nmap"
- "payload"

**Check 3**: Check server logs
- Look in `debug.log` for Telegram errors
- Search for `[DEBUG] Telegram` or `[ERROR]`

---

## 📊 Model Update

The old vision model `llama-3.2-11b-vision-preview` was deprecated by GROQ.

**Old**: llama-3.2-11b-vision-preview (❌ Decommissioned)
**New**: llama-3.1-70b-versatile (✅ Active)

Images are now processed as text descriptions instead of direct image analysis.

---

## 🎯 How It Works

1. User sends message
2. System checks for dangerous keywords (firewall)
3. If threat detected → EMERGENCY level
4. Automatically sends Telegram alert with:
   - User name
   - User email
   - Threat message
   - Timestamp

---

## 📞 Need Help?

If Telegram setup doesn't work:
1. Test bot manually: Message your bot, make sure it responds
2. Verify chat ID: Use @userinfobot to confirm your ID
3. Check api.txt format: No extra spaces, exact format shown above
4. Restart server: Changes won't apply until server restarts

---

**Server Status**: ✅ Running on http://127.0.0.1:5000
**Model**: ✅ llama-3.1-70b-versatile (Updated)
**Notifications**: ✅ UI Improvements Added
