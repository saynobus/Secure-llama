# 🔐 Sentinel AI - API Key Setup & Configuration Guide

## Overview
Sentinel AI now supports multiple ways to configure your Gemini API key and includes a fallback mode when quota is exceeded or no key is configured.

---

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Configuration Methods](#configuration-methods)
3. [Fallback Mode](#fallback-mode)
4. [Environment Variables](#environment-variables)
5. [IAM/MFA Integration](#iammfa-integration-preparation)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Option 1: Using `api.txt` (Current Setup)
Your API key is already loaded from `api.txt`. The server shows:
```
✅ API key loaded from api.txt
✅ Sentinel AI - Gemini API configured successfully
```

**To update your key:**
1. Open `api.txt` in the project root
2. Replace the current key with your new Gemini API key
3. Restart the server (`python app.py`)

### Option 2: Using Environment Variable (Recommended)
Set the `GEMINI_API_KEY` environment variable:

#### Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY = "your-gemini-api-key-here"
python app.py
```

#### Windows (Command Prompt):
```cmd
set GEMINI_API_KEY=your-gemini-api-key-here
python app.py
```

#### Windows (Permanent - System Settings):
1. Press `Win + X` → Select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables" click "New"
5. Variable name: `GEMINI_API_KEY`
6. Variable value: `your-gemini-api-key-here`
7. Click OK and restart your terminal

#### Linux/Mac:
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
python app.py
```

#### Linux/Mac (Permanent):
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

Then restart terminal or run: `source ~/.bashrc`

---

## ⚙️ Configuration Methods

### Priority Order (Checked in this sequence):
1. **Environment Variable** (`GEMINI_API_KEY`) - Highest Priority
2. **api.txt file** - Fallback file
3. **Fallback Mode** - When no key is available

### Server Startup Messages:

| Message | Meaning |
|---------|---------|
| `✅ API key loaded from environment variable GEMINI_API_KEY` | Using environment variable (recommended) |
| `✅ API key loaded from api.txt` | Using api.txt file |
| `⚠️ No API key found - Running in FALLBACK MODE (limited responses)` | No API key available - using intelligent fallback responses |

---

## 💾 Fallback Mode

### What Happens in Fallback Mode?

When your API quota is exceeded (429 error) or no API key is configured, Sentinel AI automatically switches to **Fallback Mode**:

✅ **Still Works:**
- Chat history is saved
- Messages are stored in database
- Forensic events are logged
- Responses provided on common security topics

❌ **Limited To:**
- Pre-written responses for specific topics
- Cannot analyze custom scenarios
- No image processing
- Generic security guidance only

### Supported Fallback Topics:

1. **IAM (Identity and Access Management)**
   - Authentication, Authorization, Accounting, Non-repudiation
   - Best practices for access control
   - RBAC implementation guidance

2. **MFA (Multi-Factor Authentication)**
   - Different MFA methods (something you know/have/are)
   - Setup and implementation steps
   - Security benefits and use cases

3. **Firewalls**
   - Networks security fundamentals
   - Types of firewalls
   - Security best practices

4. **Encryption**
   - Symmetric vs Asymmetric encryption
   - SSL/TLS protocol details
   - Key management practices

5. **General Security**
   - CIA Triad (Confidentiality, Integrity, Availability)
   - Common threats and defenses
   - Security audit procedures

### Triggering Fallback Responses:

Try asking about these topics when quota is exceeded:
- "Tell me about IAM"
- "How does MFA work?"
- "Explain firewalls"
- "What is encryption?"
- "Best security practices?"

---

## 🌍 Environment Variables

### GEMINI_API_KEY
- **Purpose**: Stores your Gemini API key
- **Priority**: Highest (checked first)
- **Security**: Keep it private! Don't commit to version control
- **Format**: `sk_...` or similar (depends on your API key format)

### Example `.env` File (Optional):
Create `.env` file in project root (not checked into git):
```
GEMINI_API_KEY=your-gemini-api-key-here
```

Then install `python-dotenv`:
```bash
pip install python-dotenv
```

And load it in your script (we'll automate this):
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🔑 IAM/MFA Integration Preparation

### Current Database Schema (Ready for IAM):

#### Users Table (Future)
```sql
CREATE TABLE iam_users (
    id VARCHAR(16) PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    mfa_method VARCHAR(50),  -- 'authenticator', 'sms', 'email', 'hardware'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

#### Roles Table (Future)
```sql
CREATE TABLE iam_roles (
    id VARCHAR(16) PRIMARY KEY,
    user_id VARCHAR(16) NOT NULL,
    role_name VARCHAR(100),  -- 'admin', 'analyst', 'viewer', 'contributor'
    permissions JSON,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES iam_users(id)
)
```

#### Audit Log (Future)
```sql
CREATE TABLE iam_audit_log (
    id VARCHAR(16) PRIMARY KEY,
    user_id VARCHAR(16) NOT NULL,
    action VARCHAR(100),
    resource VARCHAR(255),
    status VARCHAR(50),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES iam_users(id)
)
```

### Steps When You Provide Your IAM/MFA Key:

1. **Share Your Key** with the development team
2. **Database Updates** will be applied:
   - Add IAM tables (Users, Roles, Permissions)
   - Add MFA configuration table
   - Add audit log table
3. **Authentication Layer** will be implemented:
   - User registration/login endpoints
   - MFA verification logic
   - Session token management
4. **Authorization Checks** will be added to all endpoints
5. **Audit Logging** will track all user actions

---

## 🔧 Troubleshooting

### Issue: "No API key found - Running in FALLBACK MODE"

**Cause**: No API key in environment variable or api.txt

**Solution**:
1. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/)
2. Set environment variable:
   ```powershell
   $env:GEMINI_API_KEY = "your-key-here"
   ```
3. Or update `api.txt`:
   ```
   your-gemini-api-key-here
   ```
4. Restart server

### Issue: "Error: 429 You exceeded your current quota"

**Cause**: Free tier daily limit (20 requests/day) exceeded

**Solution Options**:
1. **Wait**: Quota resets daily at UTC midnight
2. **Upgrade**: Switch to paid Gemini API tier
3. **Use Fallback**: Already automatic - just ask about security topics
4. **Use Different Key**: If you have a paid tier key, use Option 2 above

### Issue: API key not loading from environment variable

**Solution**:
1. Verify variable is set:
   ```powershell
   $env:GEMINI_API_KEY  # Should show your key
   ```
2. Restart Python/terminal after setting env variable
3. Check spelling: `GEMINI_API_KEY` (exact case matters on Linux/Mac)
4. Fallback to `api.txt` method as alternative

### Issue: Fallback responses don't recognize my query

**Solution**: 
- Fallback mode looks for keywords like "IAM", "MFA", "firewall", "encryption", "security"
- Generic fallback response provided for unrecognized queries
- Full AI responses available when API is configured

---

## 📊 Server Status Check

### View Current Configuration:

Visit the stats endpoint:
```
GET http://localhost:5000/api/stats
```

Response shows:
- Server uptime
- Total sessions
- Total messages
- Total forensic events
- Active configuration status

### Example Response:
```json
{
  "success": true,
  "status": "running",
  "api_configured": true,
  "fallback_mode": false,
  "total_sessions": 5,
  "total_messages": 47,
  "total_forensic_events": 156,
  "database_size_bytes": 65536,
  "uptime_seconds": 3600
}
```

---

## 🎯 Next Steps

### Immediate (Today):
- ✅ Test fallback responses with security questions
- ✅ Verify environment variable support works
- ✅ Check database is storing messages correctly

### Short Term (This Week):
- [ ] Provide your own Gemini API key or use paid tier
- [ ] Enable full AI responses for all query types
- [ ] Set up permanent environment variable (if using that method)

### Medium Term (When You're Ready):
- [ ] Share IAM/MFA requirements
- [ ] Provide authentication key/credentials
- [ ] Set up user management system
- [ ] Implement role-based access control

---

## 📞 Support

### Common Commands:

**Check if server is running:**
```powershell
curl http://localhost:5000/api/stats
```

**Test chat with fallback:**
```powershell
curl -X POST http://localhost:5000/api/chat `
  -H "Content-Type: application/json" `
  -d '{
    "message": "Tell me about IAM",
    "session_id": "test"
  }'
```

**Test with your API key:**
```powershell
$env:GEMINI_API_KEY = "your-key"
python app.py
```

---

## 🔒 Security Notes

### NEVER:
- ❌ Commit API keys to Git/GitHub
- ❌ Share API keys in chat/email
- ❌ Store keys in plain text scripts
- ❌ Commit `.env` files to version control

### ALWAYS:
- ✅ Use environment variables for sensitive data
- ✅ Rotate keys regularly
- ✅ Use `.gitignore` to exclude sensitive files
- ✅ Monitor API usage for suspicious activity

---

**Last Updated**: 2025
**Sentinel AI Version**: 2.0 (With Fallback Mode)
**Status**: ✅ Production Ready
