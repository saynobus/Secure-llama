# 🛡️ Admin Host Setup Guide

## Overview

This guide explains how to run the **admin dashboard on a separate host** for enhanced security and isolation.

---

## Why Separate Admin Host?

| Aspect | Benefit |
|--------|---------|
| 🔒 **Security** | Admin panel isolated from main chat interface |
| 🌐 **Network** | Can restrict admin to internal network only |
| 🎯 **Focus** | Dedicated host for analytics & logging |
| 📊 **Performance** | No resource contention with chat server |
| 🔑 **Access Control** | Host-based restrictions + JWT auth |

---

## Two-Server Setup

### Architecture

```
┌─────────────────────────────┐
│  Main Chat Server           │
│  (Users, discussions, IDE)  │
│  http://localhost:5000      │
└─────────────────────────────┘
           ↓ (JWT Token)
┌─────────────────────────────┐
│  Admin Dashboard Server     │
│  (Analytics, Logs)          │
│  http://admin.localhost:5001│
└─────────────────────────────┘
```

---

## Setup Steps

### Terminal 1: Main Chat Server

```powershell
# Windows
cd c:\path\to\gemini-ai-chat

# Set environment variables (NO ADMIN_HOST)
$env:SECRET_KEY='mysecretkey'
$env:OPENAI_API_KEY='sk-...'

# Start on port 5000
python app.py
```

### Terminal 2: Admin Dashboard Server

```powershell
# Windows
cd c:\path\to\gemini-ai-chat

# Set ADMIN_HOST to restrict admin routes
$env:SECRET_KEY='mysecretkey'
$env:OPENAI_API_KEY='sk-...'
$env:ADMIN_HOST='admin.localhost'

# Start on port 5001 (or different port)
python app.py --port 5001
```

#### Or in Linux/Mac:

```bash
# Terminal 1 - Chat Server
export SECRET_KEY='mysecretkey'
export OPENAI_API_KEY='sk_...'
python app.py  # runs on localhost:5000

# Terminal 2 - Admin Server
export SECRET_KEY='mysecretkey'
export OPENAI_API_KEY='sk_...'
export ADMIN_HOST='admin.localhost'
flask run --port 5001
```

---

## Configuration Details

### ADMIN_HOST Variable

When you set `ADMIN_HOST`, the following happens:

1. **`/admin/dashboard`** - Only accessible from the configured host
2. **`/admin/login`** - Separate login page shown (if on admin host)
3. Other routes work normally (no restrictions)

```python
# From app.py
ADMIN_HOST = os.getenv('ADMIN_HOST', '')  # e.g. 'admin.localhost' or 'admin.mydomain.com'

if ADMIN_HOST:
    host = request.host.split(':')[0]
    allowed = ADMIN_HOST.split(':')[0]
    if host != allowed:
        return jsonify({'success': False, 'error': 'Admin panel accessible only from admin host'}), 403
```

---

## Accessing Admin Dashboard

### From Main Chat Server

When logged in to main chat:
- Click **Profile Menu** → **Admin Dashboard**
- Opens admin panel **in a new tab/window**
- Dashboard URL depends on `ADMIN_HOST` setting:
  - If `ADMIN_HOST='admin.localhost'`: opens `http://admin.localhost/admin/dashboard`
  - If not set: opens `/admin/dashboard` on same host

### Direct URL Access

```
Main Chat:    http://localhost:5000
Admin Panel:  http://admin.localhost:5001/admin/dashboard  (if separate host/port)
```

---

## Production Deployment

### Docker Compose (Separate Containers)

```yaml
version: '3.9'

services:
  chat-server:
    build: .
    ports:
      - "5000:5000"
    environment:
      SECRET_KEY: ${SECRET_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      FLASK_ENV: production
    volumes:
      - ./sentinel_ai.db:/app/sentinel_ai.db

  admin-server:
    build: .
    ports:
      - "5001:5000"
    environment:
      SECRET_KEY: ${SECRET_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      ADMIN_HOST: admin.yourdomain.com
      FLASK_ENV: production
    volumes:
      - ./sentinel_ai.db:/app/sentinel_ai.db
    depends_on:
      - chat-server
```

### Nginx Reverse Proxy

```nginx
upstream chat_server {
    server localhost:5000;
}

upstream admin_server {
    server localhost:5001;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://chat_server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    listen 80;
    server_name admin.yourdomain.com;

    location / {
        proxy_pass http://admin_server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Security Considerations

### 1. JWT Tokens

Both servers share the same database and SECRET_KEY:
- Tokens generated on main server work on admin server
- Both validate using same approach

### 2. Host Restrictions

- Admin routes check incoming `request.host`
- If `ADMIN_HOST` mismatch → **403 Forbidden**
- Can use firewall rules to further restrict access

### 3. Database Sharing

Both servers use the same `sentinel_ai.db`:
- ✅ SQLite handles concurrent reads/writes
- ✅ Both have access to user data, sessions, logs
- Use `WAL` mode for better concurrency if needed

### 4. Environment Variables

Keep these **identical** on both servers:
```
SECRET_KEY (must match for JWT validation)
OPENAI_API_KEY (both need same keys)
DATABASE_URL (optional, for remote DB)
```

Different values:
```
ADMIN_HOST (main server: empty | admin server: 'admin.host')
FLASK_PORT (chat: 5000 | admin: 5001)
```

---

## Troubleshooting

### "Admin panel accessible only from admin host" Error

**Problem:** Admin server can't access `/admin/dashboard`

**Solution:** 
1. Check `ADMIN_HOST` env var is set
2. Check request is coming from correct host
3. Use curl to debug:
```bash
# This should fail with 403
curl http://localhost:5000/admin/dashboard

# This should work (if ADMIN_HOST='admin.localhost')
curl -H "Host: admin.localhost" http://localhost:5001/admin/dashboard
```

### tokens Invalid on Admin Server

**Problem:** JWT token from main server doesn't work on admin

**Solution:**
- Ensure both servers have same `SECRET_KEY`
- Check token format is correct (Bearer token)
- Verify database connection works on admin server

### "Admin privileges required" Error

**Problem:** User not in admin role

**Solution:**
- Login with admin account
- Check database: `SELECT * FROM iam_roles WHERE role_name='admin'`
- Or assign admin role:
```sql
INSERT INTO iam_roles (user_id, role_name)
VALUES (1, 'admin');
```

---

## Quick Commands

### Windows - Two Terminals

**Terminal 1:**
```powershell
$env:OPENAI_API_KEY='sk_...'
$env:SECRET_KEY='key'
python app.py
```

**Terminal 2:**
```powershell
$env:OPENAI_API_KEY='sk_...'
$env:SECRET_KEY='key'
$env:ADMIN_HOST='admin.localhost'
python app.py --port 5001
```

### Linux - Two Terminals

**Terminal 1:**
```bash
export OPENAI_API_KEY='sk_...'
export SECRET_KEY='key'
python app.py
```

**Terminal 2:**
```bash
export OPENAI_API_KEY='sk_...'
export SECRET_KEY='key'
export ADMIN_HOST='admin.localhost'
flask run --port 5001
```

---

## Features Unlocked

✅ **Host-Restricted Admin Access** - Only from admin.host  
✅ **Separate Deployment** - Different server/container  
✅ **Same Database** - Shared forensic logs  
✅ **JWT Auth** - Tokens work across both  
✅ **Production Ready** - Scale independently  

---

## What's Next?

1. **Set up DNS/hosts file** to map admin.localhost → 127.0.0.1
2. **Configure firewall** to restrict admin access (optional)
3. **Use reverse proxy** (Nginx/Apache) for SSL/TLS
4. **Monitor both servers** with application insights
5. **Backup database** shared between servers

---

**Start with**: `export ADMIN_HOST='admin.localhost'` and run admin on separate terminal!
