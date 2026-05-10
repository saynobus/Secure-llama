# Sentinel AI - Universal Enterprise Intelligence Assistant 🛡️

**Version: 2.0-Universal** | **Status: ✅ PRODUCTION READY**

A modern, ChatGPT-style enterprise AI assistant powered by Google's Gemini 2.5-flash with **universal intelligence** capabilities. Now includes Admin Dashboard, VS Code-style IDE, complete data persistence, and Infosys Topaz-like functionality.

## 🎯 What's New in v2.0

✨ **MAJOR UPGRADE (Feb 26, 2026)**

- ✅ **Persistent Database** - All chats stored forever (never lost)
- ✅ **Offline Protection** - Server-enforced, no caching possible
- ✅ **Universal AI** - Not just security (full stack, ML, DevOps, etc.)
- ✅ **Admin Dashboard** - Real-time logs, statistics, activity monitoring
- ✅ **VS Code IDE** - Professional code editor with Sentinel AI analysis
- ✅ **Forensic Logging** - Complete audit trail of everything
- ✅ **Multi-Provider Ready** - Architecture supports any AI provider

## 📚 Documentation

- 📖 **[QUICK_START_v2.0.md](QUICK_START_v2.0.md)** - Get started in 5 minutes
- 📖 **[UPGRADE_v2.0.md](UPGRADE_v2.0.md)** - Complete feature documentation
- 📖 **[DEPLOYMENT_COMPLETE.md](DEPLOYMENT_COMPLETE.md)** - Technical details
- 📖 **[ADMIN_HOST_IMPLEMENTATION.md](ADMIN_HOST_IMPLEMENTATION.md)** - Separate admin host summary
- 📖 **[ADMIN_HOST_SETUP.md](ADMIN_HOST_SETUP.md)** - Local & Docker setup guide
- 📖 **[ADMIN_HOST_PRODUCTION.md](ADMIN_HOST_PRODUCTION.md)** - Enterprise deployment patterns

## ✨ Current Features

### Chat & AI
- 💬 Real-time chat with universal AI (like ChatGPT/Claude)
- 🎨 Modern ChatGPT-style UI
- 📝 Full markdown with code highlighting
- 🖼️ Image upload & analysis
- 📋 Complete chat history (persistent)

### Intelligence Capabilities
- 💻 **Full-stack development** - Any programming language
- ☁️ **Cloud computing** - AWS, Azure, GCP, Kubernetes, Docker
- 🤖 **AI & Machine Learning** - TensorFlow, PyTorch, Scikit-learn
- 🏗️ **System Design** - Architecture, microservices, APIs
- 🔐 **Security** - Encryption, OAuth, MFA, penetration testing
- 📊 **Data Science** - Analytics, SQL, NoSQL optimization
- 🚀 **DevOps** - CI/CD, Infrastructure, Container orchestration
- **And literally anything else** (not limited to security)

### Admin Features
- 📊 **Admin Dashboard** - Real-time statistics & monitoring
- 📋 **Activity Logs** - Complete forensic audit trail
- 🔍 **Advanced Filtering** - Search & filter logs
- 📍 **IP Tracking** - Every action tracked with IP address

### Developer Tools
- 💻 **Code IDE** - VS Code-style editor
- 🔍 **Code Analysis** - Real-time error detection
- 🤖 **Sentinel AI Integration** - Analyze code for bugs & improvements
- 📸 **Multi-language** - Python, JavaScript, Java, Go, Rust, etc.

## 🚀 Getting Started

### Quick Start (5 minutes)
```bash
# 1. Navigate to project
cd gemini-ai-chat

# 2. Start server
python app.py

# 3. Access services
Chat:   http://localhost:5000/dashboard
Admin:  http://localhost:5000/admin/dashboard
IDE:    http://localhost:5000/ide
```

### Login
- **Google OAuth** - Instant login
- **Email/Password** - Create account
- **Phone + OTP** - SMS verification

### Test Offline Protection
```
✅ Server running → Chat works
❌ Stop server → "Server offline" error appears
❌ No cached responses, no offline mode
```

### Verify Data Persistence
```
1. Chat something
2. Stop server (Ctrl+C)
3. Start server again
4. Login again
5. 🎉 Chat history still there!
```

## 📁 Project Structure

```
gemini-ai-chat/
├── app.py                           # Flask backend (UPDATED)
├── sentinel_ai.db                   # SQLite database (persistent)
├── requirements.txt                 # Dependencies
├── api.txt                         # Gemini API keys
├── templates/
│   ├── index.html                 # Main chat interface
│   ├── login.html                 # Login page
│   ├── mfa-setup.html             # MFA configuration
│   ├── admin_dashboard.html       # Admin panel (NEW)
│   └── ide.html                   # Code editor IDE (NEW)
├── README.md                        # This file
├── QUICK_START_v2.0.md             # Quick start guide (NEW)
├── UPGRADE_v2.0.md                 # Feature documentation (NEW)
└── DEPLOYMENT_COMPLETE.md          # Deployment details (NEW)
```

## ⚙️ Configuration

Set up your environment variables before running the server:

- `SECRET_KEY` – Flask secret key for session signing and JWTs.
- `OPENAI_API_KEY` – API key for the Gemini/OpenAI model you wish to use.
- `ADMIN_HOST` – **optional** host (or host:port) where the admin dashboard will be served. When provided, the `/admin` routes are restricted to requests originating from this host and a separate login page is shown. Useful for running the admin UI on a different domain/port for improved security.

## 🔐 Architecture

```
Browser (Cache-Free)
    ↓
Health Check → /api/health (forced server check)
    ↓
Authentication → JWT + Cookies
    ↓
API Requests → No-Cache Headers Applied
    ↓
Sentinel AI Engine (Universal)
    ↓
Gemini 2.5-flash API (with fallback)
    ↓
Database → Permanent Storage
    ↓
Forensic Logs → Complete Audit Trail
```

## 📊 Database

**Persistent Storage - Nothing Gets Lost**

```
sentinel_ai.db (SQLite)
├── chat_sessions       - Stored conversations
├── chat_messages       - Individual messages (PERMANENT)
├── forensic_logs       - Activity logs (PERMANENT)
├── iam_users          - User accounts
├── iam_audit_logs     - Access logs
└── [+5 more tables]
```

**Retention Policy:**
- ⏰ Chat sessions - Until manually deleted
- ⏰ Messages - Until manually deleted  
- ⏰ Logs - Until manually deleted
- ⏰ User data - Until account deleted

## 🔌 API Endpoints

### New Endpoints (v2.0)
```
GET  /api/health            - Server health check
GET  /api/chat-sessions     - Load all chat history
GET  /api/logs              - Get forensic logs
GET  /admin/dashboard       - Admin panel
GET  /ide                   - Code editor IDE
```

### Existing Endpoints
```
POST /api/chat              - Send message to AI
GET  /api/user              - Get user profile
POST /auth/google-callback  - Google OAuth
POST /auth/logout           - Logout
```

## 🛡️ Security Features

- ✅ JWT authentication (24-hour tokens)
- ✅ Password hashing (bcrypt, 12 rounds)
- ✅ Multi-factor authentication (TOTP + SMS)
- ✅ Cache prevention (no offline possible)
- ✅ Forensic logging (complete audit trail)
- ✅ IP tracking (all actions logged)
- ✅ CORS protection
- ✅ Rate limiting
- ✅ CSRF protection
- ✅ Input validation

## 📈 Performance & Reliability

- ✨ Multi-API-key rotation (3 keys supported)
- ✨ Automatic fallback responses
- ✨ Error recovery & retry logic
- ✨ Session persistence
- ✨ Database auto-backup

## 🎯 Use Cases

### Developers
- Write code in IDE → Get instant analysis
- Ask about any programming topic
- Get architecture recommendations
- Debug issues with AI assistance

### Administrators
- Monitor all user activity
- Review forensic logs
- Track system usage
- Analyze patterns & trends

### Enterprise Teams
- Universal AI for any question
- Code review automation
- Knowledge base assistant
- Internal support automation

### Security Teams
- Network architecture design
- Cloud security setup
- Compliance documentation
- Penetration testing planning

## 🚀 Deployment

### Local Development
```bash
python app.py
# Runs on http://localhost:5000
```

### Production (Coming Soon)
- Docker containerization
- AWS/Azure/GCP deployment guides
- Load balancing setup
- SSL/TLS configuration

## 📞 Support

**Documentation:**
- 📖 Quick Start: [QUICK_START_v2.0.md](QUICK_START_v2.0.md)
- 📖 Features: [UPGRADE_v2.0.md](UPGRADE_v2.0.md)
- 📖 Deployment: [DEPLOYMENT_COMPLETE.md](DEPLOYMENT_COMPLETE.md)

**Troubleshooting:**
- Server offline? `python app.py` to restart
- Chat not loading? Check `/api/health` endpoint
- Logs missing? Check Admin Dashboard
- Database issue? Delete `sentinel_ai.db` (auto-recreates)

## 🎓 Technical Stack

- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Backend:** Python, Flask, SQLAlchemy
- **Database:** SQLite3
- **AI:** Google Gemini 2.5-flash
- **Auth:** JWT, OAuth 2.0, TOTP, SMS OTP
- **Security:** bcrypt, CORS, Rate Limiting

## 📝 License

Private - Sentinel AI

## 🤝 Contributing

This is a private project. Contact maintainer for contributions.

## 📞 Contact

For issues, questions, or suggestions, please create an issue in the repository.

---

**Status:** ✅ PRODUCTION READY | **Version:** 2.0-Universal | **Last Updated:** Feb 26, 2026

**🚀 Ready to Rock!**
├── requirements.txt          # Python dependencies
├── api.txt                   # Your Gemini API key
├── README.md                 # This file
├── uploads/                  # Image/file uploads directory
└── templates/
    └── index.html           # Complete frontend (HTML+CSS+JS)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- Modern web browser

### Installation

1. **Clone/Setup the project:**
```bash
cd gemini-ai-chat
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Add your API key:**
Edit `api.txt` and paste your Gemini API key on the first line:
```
AIzaSy...your_key_here...
```

4. **Run the server:**
```bash
python app.py
```

5. **Open in browser:**
Navigate to `http://localhost:5000`

## 🎮 Usage

### Text Chat
- Type a message in the input field
- Press `Ctrl+Enter` or `Cmd+Enter` to send
- Click send button or use keyboard shortcut

### Image Analysis
- Click the **📷 Image** button
- Select an image from your device
- Add text question about the image
- Send to get AI analysis

### Voice Input
- Click the **🎤 Microphone** button to record
- Click again to stop recording
- (Transcription service coming soon)

### Chat History
- View all previous messages in the left sidebar
- Click any previous conversation to reload
- Create new chats with the "New Chat" button

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send message with optional image |
| POST | `/api/clear-chat` | Clear conversation history |
| GET | `/api/history` | Get chat messages for session |
| GET | `/api/sessions` | List all chat sessions |

### Example Request
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain this image",
    "session_id": "session_123",
    "image": "data:image/png;base64,..."
  }'
```

## 🎨 Customization

### Change UI Theme
Edit CSS variables in `templates/index.html` (lines 18-27):
```css
:root {
    --primary-bg: #ffffff;
    --accent-color: #10a37f;
    /* ... more colors ... */
}
```

### Modify System Instructions
Edit `app.py` line 64-71 to change AI behavior

### Change AI Model
Edit `app.py` line 32:
```python
MODEL_NAME = 'gemini-2.5-flash'  # or any other available model
```

## 🔐 Security

- API key stored locally in `api.txt` (not in code)
- CORS enabled for local development
- Conversation history stored in memory (not persisted)
- No data sent to external services except Gemini API

## 📋 Current Limitations & Coming Soon

- [ ] Voice transcription (ready, needs speech-to-text service)
- [ ] Persistent chat history (database needed)
- [ ] File upload support (docs, PDFs, etc.)
- [ ] Authentication & user accounts
- [ ] Firewall policy builder
- [ ] DLP rule generator
- [ ] IAM assistant
- [ ] MFA setup guide

## 🛠️ Troubleshooting

### Port Already in Use
```bash
python app.py  # Will try port 5000
# Change in app.py line 171: app.run(debug=True, port=5001)
```

### API Key Errors
- Verify key is on first line of `api.txt`
- Check key is valid at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Ensure no extra spaces or newlines

### Images Not Processing
- Check file is valid PNG/JPG/GIF/WEBP
- Image size should be < 20MB
- Verify Gemini API supports image analysis

### Microphone Not Working
- Grant browser microphone permissions
- Check browser security settings
- Try HTTPS or localhost

## 📊 Model Information

**Current Model:** `gemini-2.5-flash`
- Fast and efficient
- Supports text, images, and code
- ~0.075 USD per 1M input tokens
- ~0.3 USD per 1M output tokens

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
Create `Dockerfile`:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

## 📝 License

Open source - modify and use freely for your projects

## 🤝 Contributing

Suggestions and improvements welcome! The roadmap includes enterprise security features.

## 📞 Support

- Check README troubleshooting section
- Review API documentation
- Test with sample images first

---

**Made with ❤️ for Security Professionals** | v1.0 | Built on Gemini API
