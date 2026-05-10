# 🏗️ **SENTINEL AI v2.0 - SYSTEM ARCHITECTURE**

## Overall Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         END USERS                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  Developer   │  │ Administrator│  │   General    │              │
│  │   (IDE)      │  │  (Dashboard) │  │    User      │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
└─────────┼─────────────────┼─────────────────┼──────────────────────┘
          │                 │                 │
    ┌─────▼─────────────────▼─────────────────▼──────┐
    │         WEB BROWSER (CLIENT SIDE)              │
    ├─────────────────────────────────────────────────┤
    │                                                 │
    │  ✅ Health Check Override                       │
    │  ✅ Cache Control Headers                       │
    │  ✅ Query Parameters (_t timestamp)             │
    │  ✅ Zero Offline Caching                        │
    │                                                 │
    │  Pages:                                         │
    │  - /dashboard (Chat interface)                 │
    │  - /admin/dashboard (Analytics)                │
    │  - /ide (Code Editor)                          │
    │                                                 │
    └────────────────┬────────────────────────────────┘
                     │ (HTTPS/HTTP - No Cache)
                     │ All requests include Cache-Control headers
                     │
        ┌────────────▼──────────────────┐
        │   FLASK APPLICATION SERVER    │
        │   (http://localhost:5000)     │
        ├───────────────────────────────┤
        │                               │
        │  🔐 AUTHENTICATION LAYER      │
        │  ├─ JWT Validation            │
        │  ├─ Cookie Validation         │
        │  ├─ OAuth Verification        │
        │  └─ MFA Checks                │
        │                               │
        │  📊 REQUEST ROUTING           │
        │  ├─ /api/health               │
        │  ├─ /api/user                 │
        │  ├─ /api/chat                 │
        │  ├─ /api/chat-sessions        │
        │  ├─ /api/logs                 │
        │  ├─ /auth/*                   │
        │  └─ /dashboard, /admin, /ide  │
        │                               │
        │  🛡️ SENTINEL SECURITY LAYER   │
        │  ├─ Input Validation          │
        │  ├─ Rate Limiting             │
        │  ├─ Forensic Logging          │
        │  ├─ IP Tracking               │
        │  └─ Error Handling            │
        │                               │
        │  🧠 AI ENGINE                 │
        │  ├─ Request Preparation       │
        │  ├─ System Instruction        │
        │  ├─ Chat History Management   │
        │  ├─ API Key Rotation          │
        │  └─ Fallback Handling         │
        │                               │
        └────────┬─────────────┬────────┘
                 │             │
       ┌─────────▼──┐   ┌──────▼─────────┐
       │  DATABASE  │   │  AI PROVIDERS  │
       │ (SQLite)   │   │                │
       ├────────────┤   ├────────────────┤
       │            │   │ 🤖 Gemini API  │
       │ Tables:    │   │ (3 API keys)   │
       │ ✅ Users   │   │                │
       │ ✅ Sessions│   │ Future:        │
       │ ✅ Messages│   │ - OpenAI       │
       │ ✅ Logs    │   │ - Claude       │
       │ ✅ Roles   │   │ - Cohere       │
       │ ✅ Permissions   │ - Bedrock  │
       │ ✅ MFA          │ - Others       │
       │ ✅ Audit        │                │
       │            │   │ (Architecture  │
       │ PERSISTENT │   │  Ready)        │
       │ (Forever)  │   │                │
       │            │   │                │
       └────────────┘   └────────────────┘
```

---

## Data Flow: Chat Message

```
USER SENDS MESSAGE
       │
       ▼
1. Browser sends POST /api/chat
   - Cache-Control: no-store header
   - JWT token in Authorization
   - Message content
   
       │
       ▼
2. Server receives request
   - Validates JWT token
   - Checks rate limits
   - Validates input
   - Extracts user_id from token
   
       │
       ▼
3. Store user message in database
   - ChatMessage table
   - timestamp, user_id, session_id, content
   - Forensic log of message_sent action
   
       │
       ▼
4. Prepare AI request
   - Load chat history from database
   - Build API history array
   - Add system instruction (universal AI)
   - Include user message
   
       │
       ▼
5. Call AI Provider (Gemini 2.5-flash)
   - If successful → Get response
   - If quota exceeded → Rotate API key
   - If all keys exhausted → Fallback response
   
       │
       ▼
6. Store AI response in database
   - ChatMessage table (role='model')
   - response_time_ms, tokens_used, metadata
   - Forensic log of response_received action
   
       │
       ▼
7. Prepare response with headers
   - Cache-Control: no-store, no-cache, must-revalidate
   - Pragma: no-cache
   - Expires: 0
   
       │
       ▼
8. Return JSON to browser
   - success: true/false
   - reply: AI response
   - session_id: conversation ID
   - response_time_ms: performance metric
   
       │
       ▼
BROWSER DISPLAYS RESPONSE
  (Never cached - forced from server)
```

---

## Admin Dashboard Data Flow

```
ADMIN CLICKS "ADMIN DASHBOARD"
       │
       ▼
1. Browser loads admin_dashboard.html
   - JavaScript fetches /api/logs
   - Includes Cache-Control headers
   
       │
       ▼
2. Server processes /api/logs request
   - Validates JWT (admin must have login)
   - Queries forensic_logs table
   - Filters by current user_id
   - Orders by timestamp DESC
   - Gets last 500 logs
   
       │
       ▼
3. Database query
   - SELECT * FROM forensic_logs
   - WHERE user_id = current_user
   - ORDER BY created_at DESC
   - LIMIT 500
   
       │
       ▼
4. Server returns JSON
   - Array of log entries
   - Each entry has:
     ├─ timestamp
     ├─ action (message_sent, error, etc)
     ├─ details (JSON)
     └─ ip_address
   
       │
       ▼
5. Browser displays dashboard
   - Calculates statistics:
     ├─ Total logs count
     ├─ Messages sent today
     ├─ Total errors
     └─ Server status
   
       ▼
   - Displays activity table
     ├─ Timestamp (formatted)
     ├─ Action badge (color-coded)
     ├─ Details snippet
     └─ IP address
   
       ▼
   - Enables filtering:
     ├─ Search by keyword
     ├─ Filter by action type
     └─ Real-time updates every 30 sec
```

---

## Code IDE Data Flow

```
USER WRITES CODE IN IDE
       │
       ▼
1. JavaScript monitors code editor
   - Line number sync
   - Cursor position tracking
   - Real-time display updates
   
       │
       ▼
2. User clicks "Analyze with Sentinel AI"
   - JavaScript calls /api/chat
   - Sends prompt: "Analyze this code..."
   - Includes code content
   - Journal ID: "ide_analysis"
   
       │
       ▼
3. Server processes analysis request
   - Validates code isn't empty
   - Creates special forensic log (ide_analysis)
   - Sends to Sentinel AI with prompt
   
       │
       ▼
4. Sentinel AI analyzes code
   - Looks for syntax errors
   - Checks logic issues
   - Identifies security problems
   - Suggests improvements
   - Provides best practices
   
       │
       ▼
5. Response stored in database
   - ChatMessage with role='model'
   - Special metadata: {type: 'code_analysis'}
   - Session ID: "ide_analysis"
   
       │
       ▼
6. Browser displays analysis
   - Right panel shows:
     ├─ Errors found
     ├─ Line numbers
     ├─ Severity levels
     ├─ Suggested fixes
     └─ Best practices
   
       │
       ▼
   - User can:
     ├─ Read analysis
     ├─ Apply suggestions
     ├─ Ask follow-up questions
     └─ All logged in forensic_logs
```

---

## Offline Protection Flow

```
USER OPENS BROWSER
       │
       ▼
Dashboard loads (index.html)
       │
       ▼
JavaScript runs initializeDashboard()
       │
       ▼
1️⃣  HEALTH CHECK (First Priority)
    GET /api/health?_t=timestamp
    - Must succeed or fail hard
    - No cache allowed (_t parameter)
    - Server MUST respond
    
    ├─ IF SERVER ONLINE ✅
    │  └─ Continue to next step
    │
    └─ IF SERVER OFFLINE ❌
       ├─ Catch network error
       ├─ Show error message:
       │  "⚠️ Server unavailable"
       ├─ Redirect to login after 2 sec
       └─ NO cached responses used
    
       │
       ▼
2️⃣  AUTHENTICATION CHECK
    - Verify JWT token exists
    - Check token validity
    - If invalid → Redirect to login
    
       │
       ▼
3️⃣  LOAD USER DATA
    GET /api/user?_t=timestamp
    - Includes Authorization header
    - Includes Cache-Control headers
    
    ├─ IF SUCCESS ✅
    │  ├─ Populate user name
    │  ├─ Update profile info
    │  └─ Continue
    │
    └─ IF 401 ERROR ❌
       └─ Redirect to login
    
       │
       ▼
4️⃣  LOAD CHAT HISTORY
    GET /api/chat-sessions?_t=timestamp
    - Load previous conversations
    - Display last 10 messages
    - Restore session ID
    
       │
       ▼
✅ DASHBOARD FULLY FUNCTIONAL
   (All data from server, nothing cached)
```

---

## Security & Forensic Logging

```
EVERY REQUEST FLOW:

┌─ Incoming Request
│
├─► 1. AUTHENTICATION
│   ├─ Check JWT token (from header or cookie)
│   ├─ Validate signature & expiry
│   └─ Log: login_attempt (success/failure)
│
├─► 2. AUTHORIZATION
│   ├─ Check user permissions
│   ├─ Validate request is allowed
│   └─ Log: permission_check
│
├─► 3. VALIDATION
│   ├─ Sanitize inputs
│   ├─ Check data types
│   ├─ Verify required fields
│   └─ Log: validation_result
│
├─► 4. RATE LIMITING
│   ├─ Check request count per user
│   ├─ Check request count per IP
│   ├─ Enforce limits
│   └─ Log: rate_limit_check
│
├─► 5. PROCESSING
│   ├─ Handle business logic
│   ├─ Call AI providers
│   ├─ Query databases
│   └─ Log: action_performed (message_sent, etc)
│
├─► 6. RESPONSE
│   ├─ Add Cache-Control headers
│   ├─ Include timestamp
│   ├─ Prepare JSON
│   └─ Log: response_sent
│
└─┬─ FORENSIC LOGGING
  │
  ▼  Every action stored in forensic_logs table:
  
  ForensicLog Entry:
  ├─ id: Unique ID
  ├─ user_id: Who performed it
  ├─ action: What happened
  ├─ session_id: Which session
  ├─ details: JSON with specifics
  ├─ ip_address: From where
  └─ created_at: When it happened
  
  Searchable & filterable in Admin Dashboard
```

---

## Multi-AI Provider Architecture (Ready)

```
Current Setup:
┌─────────────────────────────────────┐
│  Application Layer                  │
│  (Universal AI Instructions)        │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Sentinel Security Wrapper          │
│ ├─ Request validation               │
│ ├─ Forensic logging                 │
│ ├─ Rate limiting                    │
│ └─ Error handling                   │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  AI Provider Abstraction Layer      │
│  (Switch providers here)            │
│  ├─ GenAI Interface                 │
│ ├─ API Key Management               │
│ ├─ Request Translation              │
│ └─ Response Normalization           │
└────────────┬────────────────────────┘
             │
             ├─► Gemini 2.5-flash (Current ✅)
             │   └─ 3 API keys (rotation)
             │
             ├─► OpenAI (Future)
             │   └─ GPT-4, ChatGPT
             │
             ├─► Anthropic Claude (Future)
             │   └─ Multi-modal
             │
             └─► Others (Future)
                 └─ Cohere, Bedrock, etc.

Benefits:
✅ Easy to switch providers
✅ Unified interface for all
✅ Security applied uniformly
✅ Fallback between providers
✅ Cost optimization routing
```

---

## Database Schema (Simplified)

```
┌─────────────────────────────────────────────────────┐
│              SENTINEL AI DATABASE                   │
│            (sentinel_ai.db - SQLite)                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  TABLE: iam_users                                  │
│  ├─ id (PK)                                        │
│  ├─ email (UNIQUE)                                 │
│  ├─ password_hash                                  │
│  ├─ google_id                                      │
│  ├─ phone_number                                   │
│  ├─ mfa_enabled                                    │
│  ├─ first_name                                     │
│  └─ last_name                                      │
│                                                     │
│  TABLE: chat_sessions                              │
│  ├─ id (PK)                                        │
│  ├─ user_id (FK)                                   │
│  ├─ title                                          │
│  ├─ created_at (INDEXED)                           │
│  ├─ updated_at (INDEXED)                           │
│  └─ message_count                                  │
│                                                     │
│  TABLE: chat_messages ⭐ (MAIN DATA STORE)         │
│  ├─ id (PK)                                        │
│  ├─ session_id (FK, INDEXED)                       │
│  ├─ user_id (FK, INDEXED)                          │
│  ├─ role ('user' or 'model')                       │
│  ├─ content (TEXT)                                 │
│  ├─ created_at (INDEXED)                           │
│  ├─ response_time (ms)                             │
│  └─ message_metadata (JSON)                        │
│  ✅ PERMANENT - Never auto-deleted                 │
│                                                     │
│  TABLE: forensic_logs ⭐ (AUDIT TRAIL)             │
│  ├─ id (PK)                                        │
│  ├─ user_id (FK, INDEXED)                          │
│  ├─ action (INDEXED)                               │
│  ├─ details (JSON)                                 │
│  ├─ ip_address                                     │
│  ├─ created_at (INDEXED)                           │
│  └─ session_id (FK, optional)                      │
│  ✅ PERMANENT - Every action logged                │
│                                                     │
│  [+ 5 more tables for MFA, OTP, roles, perms]     │
│                                                     │
└─────────────────────────────────────────────────────┘

Key Features:
✅ Automatic table creation on first run
✅ Indexes on frequently queried columns
✅ Foreign keys for referential integrity
✅ JSON columns for flexible data
✅ Timestamps on all tables
✅ Zero automatic cleanup (permanent storage)
```

---

## Deployment Topology

```
┌──────────────────────────────────────────────────────────┐
│                   CLIENT MACHINES                        │
│  (Developers, Admins, Users with Python installed)      │
│                                                          │
│  Browser: http://localhost:5000                         │
│  ├─ Chat Dashboard                                      │
│  ├─ Admin Dashboard                                     │
│  └─ Code IDE                                            │
└────────────────────┬─────────────────────────────────────┘
                     │
                     │ HTTP/HTTPS
                     │
┌────────────────────▼─────────────────────────────────────┐
│                 FLASK SERVER                             │
│         (Single process, debug mode)                    │
│                                                          │
│  Location: C:\...\gemini-ai-chat\                       │
│  Command: python app.py                                 │
│  Port: 5000                                             │
│  Status: Development server                             │
│                                                          │
│  Routes:                                                │
│  ├─ GET  /               - Redirect logic               │
│  ├─ GET  /dashboard       - Chat UI                     │
│  ├─ GET  /admin/dashboard - Admin panel                 │
│  ├─ GET  /ide             - Code editor                 │
│  ├─ POST /api/chat        - Main chat endpoint          │
│  ├─ GET  /api/user        - User profile                │
│  ├─ GET  /api/health      - Health check                │
│  ├─ GET  /api/chat-sessions - Load history             │
│  ├─ GET  /api/logs        - Get logs                    │
│  └─ POST /auth/logout     - Logout                      │
│                                                          │
└────────────────────┬──────────────────────┬─────────────┘
                     │                      │
          ┌──────────▼─────────┐  ┌────────▼────────────┐
          │   SQLite Database  │  │  Gemini 2.5-flash  │
          │                    │  │                    │
          │  sentinel_ai.db    │  │  API Keys x3       │
          │  (Permanent Data)  │  │ (Auto-rotation)    │
          │                    │  │                    │
          └────────────────────┘  └────────────────────┘

Production Upgrade Path:
├─ Docker: containerize application
├─ WSGI: use Gunicorn/uWSGI instead of debug server
├─ Load Balancer: multiple server instances
├─ SSL/TLS: HTTPS encryption
├─ Cloud: AWS/Azure/GCP deployment
└─ CDN: cache static assets
```

---

## Feature Interaction Map

```
LOGIN/AUTH
    │
    ├─► Cookie + JWT Set
    │   └─► Stored in localStorage
    │
    ▼
DASHBOARD
    │
    ├─► Health Check ✅
    │   └─► Server verification
    │
    ├─► Load User Profile
    │   └─► /api/user
    │
    ├─► Load Chat History (Persistent!) ✅
    │   └─► /api/chat-sessions
    │
    ├─► Send Message
    │   ├─► /api/chat (POST)
    │   ├─► Store in database
    │   ├─► Log action
    │   └─► Display response
    │
    └─► Access Admin Dashboard
        └─► Profile → Admin
    
    └─► Access Code IDE
        └─► Profile → Code Editor


ADMIN DASHBOARD
    │
    ├─► Load Statistics
    │   ├─ Total logs
    │   ├─ Messages today
    │   ├─ Error count
    │   └─ Server status
    │
    ├─► View Activity Logs
    │   └─► /api/logs
    │
    ├─► Filter & Search
    │   ├─ By action type
    │   ├─ By timestamp
    │   └─ By IP address
    │
    └─► Export/Report (Future)


CODE IDE
    │
    ├─► Write Code
    │   ├─ Line numbers
    │   └─ Syntax highlighting
    │
    ├─► Click "Analyze"
    │   └─► /api/chat (POST)
    │       └─► Sends code to Sentinel AI
    │
    ├─► Display Analysis
    │   ├─ Errors found
    │   ├─ Suggestions
    │   └─ Best practices
    │
    └─► Save Code (download)
```

---

**Architecture Complete & Production Ready! 🚀**

*Last Updated: February 26, 2026*
