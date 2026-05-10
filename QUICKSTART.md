# 🎬 Sentinel AI - Quick Start & Feature Guide

## 🚀 Getting Started

### Step 1: Visit the Application
```
Open browser: http://localhost:5000
```

### Step 2: See the Professional UI
The interface features:
- **Left Sidebar**: Chat history with purple gradient header
- **Main Chat Area**: Clean white background with smooth animations
- **Input Bar**: Gradient purple send button with image/voice buttons
- **Header**: Status indicator showing "Online"

### Step 3: Start Chatting
1. Type your question in the input field
2. Press **Ctrl+Enter** or click the **Send Button** (📤)
3. Watch the typing indicator (3 animated dots)
4. AI responds with formatted text including code blocks

## 💡 Feature Showcase

### 1. Text Chat
**Try**: "What is MFA and why is it important?"

The AI will:
- ✅ Respond with detailed security guidance
- ✅ Format response with markdown
- ✅ Show response time in milliseconds
- ✅ Store in database with timestamp

### 2. Image Upload
**Try**: Click 📷 → Select any image

The AI will:
- ✅ Analyze the image
- ✅ Provide description
- ✅ Compare against security context
- ✅ Store image hash in database

### 3. Voice Input (Framework Ready)
**Try**: Click 🎤 → Speak

Current state:
- 🎤 Microphone permission handled
- 🎤 Recording UI working
- ⏳ Transcription service ready for integration

### 4. Chat History
**In Sidebar**: See chat previews
- Click any previous chat to reload
- All messages persisted in database
- Timestamps on every message

### 5. Multiple Sessions
**Try**: Click "New Chat" button
- Creates new independent session
- Each session has separate history
- Separate forensic tracking
- Session ID auto-generated

## 📊 Viewing Data

### Option 1: Browser Console
```javascript
// View raw API response
fetch('/api/stats').then(r => r.json()).then(console.log)
```

### Option 2: API Curl Commands

```bash
# Get all sessions
curl http://localhost:5000/api/sessions

# Get specific chat history
curl "http://localhost:5000/api/history?session_id=<session_id>"

# Get forensic logs (last 24 hours)
curl "http://localhost:5000/api/forensics?hours=24&limit=20"

# Get forensic analysis
curl "http://localhost:5000/api/forensics/analysis?hours=24"

# Get system stats
curl http://localhost:5000/api/stats
```

### Option 3: Python Script

```python
import requests

# Get session info
r = requests.get('http://localhost:5000/api/sessions')
sessions = r.json()['sessions']

for session in sessions:
    print(f"Session: {session['id']}")
    print(f"  Title: {session['title']}")
    print(f"  Messages: {session['message_count']}")
    print(f"  Created: {session['created_at']}")
```

## 🔍 Forensic Data Examples

### Chat Message Event
```json
{
  "id": "554a1dea-bdd4-41b7-8805-5078a85df79a",
  "session_id": "ef79da22-3980-4e28-a915-f0741ac9b81e",
  "user_id": "9fac7a5b2e1d4c8f",
  "action": "message_sent",
  "details": {
    "response_time_ms": 3182.00421333313,
    "has_image": false
  },
  "ip_address": "127.0.0.1",
  "timestamp": "2026-02-25T11:57:16.816868"
}
```

### Image Upload Event
```json
{
  "action": "image_uploaded",
  "details": {
    "size": 45234
  },
  "ip_address": "127.0.0.1",
  "timestamp": "2026-02-25T12:00:00.000000"
}
```

### Error Event
```json
{
  "action": "chat_error",
  "details": {
    "error": "Connection timeout"
  },
  "ip_address": "127.0.0.1",
  "timestamp": "2026-02-25T12:01:00.000000"
}
```

## 📈 Analytics Example

```json
{
  "analysis": {
    "time_period_hours": 24,
    "total_events": 5,
    "total_sessions": 2,
    "total_messages": 12,
    "avg_response_time_ms": 3182.00,
    "events_by_action": {
      "message_sent": 8,
      "image_uploaded": 2,
      "chat_error": 1,
      "chat_cleared": 0
    }
  }
}
```

## 🎨 UI Features

### Animations
- 🌊 Floating sidebar icon (auto-repeat)
- ⌨️ Typing dots (pulsing animation)
- 📨 Slide-in messages (smooth entry)
- 🔘 Hover effects on all buttons
- 🌀 Scale animations on hover

### Design Elements
- Gradient buttons (purple → pink)
- Rounded corners (10-16px)
- Smooth shadow effects
- Color-coded message types:
  - User: Blue gradient
  - AI: Light blue gradient
  - Error: Red gradient

### Responsive Behavior
- Desktop: Full sidebar visible
- Tablet: Sidebar adjusts width
- Mobile: Sidebar hidden (700px)
- Textarea: Auto-expands (up to 120px)

## 🔐 Privacy & Security

### Data Protection
- ✅ User-Agent hashing (one-way, non-reversible)
- ✅ No passwords stored
- ✅ No personal information stored
- ✅ IP address logged only for security audit
- ✅ All timestamps in UTC for consistency

### Session Isolation
- ✅ Each user ID has isolated sessions
- ✅ Messages cannot cross-pollinate
- ✅ No shared data between users
- ✅ Forensic logs unique per user

## 🛠️ Database Structure

### ChatSession Table
```
id (UUID) → ef79da22-3980-4e28-a915-f0741ac9b81e
user_id (hash) → 9fac7a5b2e1d4c8f
title (string) → "Hello Sentinel AI, what security..."
message_count (number) → 2
created_at (datetime) → 2026-02-25 11:57:13
updated_at (datetime) → 2026-02-25 11:57:16
```

### ChatMessage Table
```
id (UUID) → msg-uuid-12345
session_id (foreign key) → session-uuid-12345
user_id (hash) → 9fac7a5b2e1d4c8f
role → "user" or "model"
content → Message text
response_time → 3182.00 (milliseconds)
created_at → 2026-02-25 11:57:13
```

### ForensicLog Table
```
id (UUID) → log-uuid-12345
session_id (foreign key) → session-uuid-12345
user_id (hash) → 9fac7a5b2e1d4c8f
action → "message_sent"
details → JSON object with metadata
ip_address → 127.0.0.1
created_at → 2026-02-25 11:57:13
```

## 🐛 Troubleshooting

### Issue: No Response from AI
**Solution**:
1. Check internet connection
2. Verify API key in `api.txt`
3. Check server console for errors
4. Restart server: `python app.py`

### Issue: Images Not Uploading
**Solution**:
1. Ensure file is actual image (JPG, PNG, etc)
2. Check browser console for errors
3. Verify Pillow is installed: `pip show pillow`

### Issue: Chat History Not Showing
**Solution**:
1. Check database file exists: `sentinel_ai.db`
2. Verify session_id is correct
3. Use `/api/history?session_id=<id>` endpoint
4. Check if messages exist in forensic logs

### Issue: Voice Input Not Working
**Solution**:
1. Grant microphone permission
2. Check browser security settings
3. Use Chrome/Firefox for best support
4. Voice transcription service is ready (use 3rd party API)

## 🌐 Advanced Usage

### Filter Forensic Logs by Hour Range
```bash
# Last 7 days
curl "http://localhost:5000/api/forensics?hours=168"

# Last 1 hour
curl "http://localhost:5000/api/forensics?hours=1"
```

### Export Chat History
```python
import requests
import json

session_id = "your-session-id"
response = requests.get(f'http://localhost:5000/api/history?session_id={session_id}')
history = response.json()['history']

# Save to file
with open('chat_export.json', 'w') as f:
    json.dump(history, f, indent=2)
```

### Monitor System Health
```python
import requests

stats = requests.get('http://localhost:5000/api/stats').json()['stats']
analysis = requests.get('http://localhost:5000/api/forensics/analysis').json()['analysis']

print(f"Avg Response Time: {analysis['avg_response_time_ms']:.2f}ms")
print(f"Total Sessions: {stats['total_sessions']}")
print(f"Total Events: {stats['total_forensic_events']}")
```

## 📚 Learning Resources

### Security Topics Covered
- Firewall Configuration
- DLP (Data Loss Prevention)
- IAM (Identity Access Management)
- MFA (Multi-Factor Authentication)
- Threat Analysis
- General Cybersecurity

### Ask These Questions
1. "What are firewall best practices?"
2. "How do I implement MFA?"
3. "Explain DLP strategies"
4. "What is IAM and why is it important?"
5. "Analyze potential security threats"

## ✅ Verification Checklist

- [ ] Server running on http://localhost:5000
- [ ] UI loads with gradient sidebar
- [ ] Can send and receive messages
- [ ] Messages appear with timestamps
- [ ] Chat history persists
- [ ] Forensic logs recorded
- [ ] Analytics showing in `/api/forensics/analysis`
- [ ] Database file (sentinel_ai.db) exists
- [ ] Status shows "Online"

## 🎉 You're All Set!

Your Sentinel AI chatbot is fully operational with:
- ✅ Professional UI
- ✅ Database persistence
- ✅ Complete forensic logging
- ✅ Advanced analytics
- ✅ Security features

**Happy chatting! 🚀**

---

**Support**: Check PROJECT_SUMMARY.md for implementation details
**Documentation**: See FEATURES.md for complete feature list
