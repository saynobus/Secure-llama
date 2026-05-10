# ⚙️ Admin Host & Separate Deployment Guide

**Status:** ✅ Fully Implemented  
**Version:** v2.0+  
**Last Updated:** 2025

---

## 🎯 What You Now Have

### Separate Admin Dashboard Host Support

The Sentinel AI system now supports **hosting the admin dashboard on a completely separate server instance** with the same codebase. This provides:

- 🔒 **Security Isolation** - Admin routes restricted to specific host
- 🌐 **Network Restriction** - Admin accessible only from internal network or specific domain
- 📊 **Shared Database** - Both servers read/write to same `sentinel_ai.db`
- 🔑 **JWT Token Sharing** - Admin users can log in from both servers with same credentials
- 🎯 **Independent Scaling** - Run chat and admin on different infrastructure

---

## 🔧 How It Works

### Configuration Method

Settings are controlled via the **`ADMIN_HOST`** environment variable:

```python
ADMIN_HOST = os.getenv('ADMIN_HOST', '')  # Empty = no restriction
```

### Three Scenarios

| Scenario | ADMIN_HOST | Result |
|----------|-----------|--------|
| **Single Server** | (not set or empty) | `/admin/dashboard` accessible from anywhere |
| **Separate Host** | `'admin.localhost'` | `/admin/dashboard` restricted to host `admin.localhost` |
| **Separate Domain** | `'admin.company.com'` | `/admin/dashboard` restricted to domain `admin.company.com` |

### Behavior

**When ADMIN_HOST is NOT set:**
```
http://localhost:5000/admin/dashboard  ✅ Works
http://localhost:5000/dashboard        ✅ Works
```

**When ADMIN_HOST='admin.localhost':**
```
http://localhost:5000/admin/dashboard        ❌ Forbidden (403)
http://admin.localhost:5000/admin/dashboard  ✅ Works
```

---

## 🚀 Quick Setup Examples

### Example 1: Single Machine, Two Ports

**Terminal 1 - Main Chat Server (Port 5000):**
```powershell
$env:OPENAI_API_KEY='sk-...'
$env:SECRET_KEY='supersecret'
# NO ADMIN_HOST set
python app.py
```

Visit: `http://localhost:5000`

**Terminal 2 - Admin Server (Port 5001):**
```powershell
$env:OPENAI_API_KEY='sk-...'
$env:SECRET_KEY='supersecret'
$env:ADMIN_HOST='admin.localhost'
python app.py --port 5001
```

Update local `hosts` file:
```
127.0.0.1    admin.localhost
```

Visit: `http://admin.localhost:5001/admin/dashboard`

---

### Example 2: Separate Machines

**Machine A (192.168.1.100) - Chat Server:**
```bash
export OPENAI_API_KEY='sk-...'
export SECRET_KEY='supersecret'
# NO ADMIN_HOST
python app.py
```

**Machine B (192.168.1.101) - Admin Server:**
```bash
export OPENAI_API_KEY='sk-...'
export SECRET_KEY='supersecret'
export ADMIN_HOST='192.168.1.101'
python app.py
```

From user's computer:
```
Chat:  http://192.168.1.100:5000
Admin: http://192.168.1.101:5000/admin/dashboard
```

---

### Example 3: Docker Compose (Production)

```yaml
version: '3.9'
services:
  chat:
    build: .
    ports:
      - "5000:5000"
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      SECRET_KEY: ${SECRET_KEY}
      FLASK_ENV: production
    volumes:
      - ./sentinel_ai.db:/app/sentinel_ai.db

  admin:
    build: .
    ports:
      - "5001:5000"
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      SECRET_KEY: ${SECRET_KEY}
      ADMIN_HOST: admin.yourdomain.com
      FLASK_ENV: production
    volumes:
      - ./sentinel_ai.db:/app/sentinel_ai.db
    depends_on:
      - chat
```

---

## 🔐 Security Architecture

### Host Restriction Logic

```python
@require_admin  # Decorator that checks admin role
def admin_dashboard():
    """Serve the admin dashboard page"""
    
    # First check: Is request from admin host?
    if ADMIN_HOST:
        host = request.host.split(':')[0]  # Extract hostname without port
        allowed = ADMIN_HOST.split(':')[0]
        if host != allowed:
            return jsonify({'success': False, 'error': 'Admin panel accessible only from admin host'}), 403
    
    # Second check: Does user have admin role?
    user = request.current_user
    db = Session()
    try:
        role = db.query(IAMRole).filter_by(user_id=user.id, role_name='admin').first()
        if not role:
            return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
    finally:
        db.close()
    
    return render_template('admin_dashboard.html')
```

### Two-Layer Protection

1. **Host Restriction** (Network/DNS level)
   - If ADMIN_HOST set, only that host can access admin routes
   - Returns 403 Forbidden otherwise

2. **Role-Based Access Control** (Application level)
   - Even if host matches, user must have `admin` role
   - Checked against `iam_roles` table

---

## 📱 User Experience

### From Chat Dashboard

When logged in to main chat, clicking **"Admin Dashboard"** in profile menu:

```javascript
function openAdminPanel() {
    const adminHost = "{{ admin_host }}";  // Passed from render_template
    
    if (adminHost && adminHost !== "") {
        // Admin is on separate host
        window.open(`http://${adminHost}/admin/dashboard`, '_blank');
    } else {
        // Admin is on same host
        window.location.href = '/admin/dashboard';
    }
}
```

**Result:**
- If admin running on same server → Opens `/admin/dashboard` tab
- If admin running on separate host → Opens new window to that host

---

## 🗄️ Database Sharing

### Both Servers Access Same DB

```
sentinel_ai.db (SQLite)
├── chat_sessions    (both read/write)
├── chat_messages    (both read/write)
├── forensic_logs    (both read/write)
├── iam_users        (both read)
├── iam_roles        (both read)
└── [other tables]
```

### Concurrency Handling

SQLite handles concurrent access:
```python
# app.py - Both servers use same connection string
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///sentinel_ai.db')
```

For production with higher concurrency, consider:
- PostgreSQL instead of SQLite
- Add connection pool configuration
- Enable WAL mode: `pragma journal_mode=wal`

---

## 🌐 Network Topology

### Single Machine, Multiple Ports
```
User Browser
    ↓
    ├→ http://localhost:5000          (Main Chat)
    └→ http://admin.localhost:5001    (Admin Panel)
         ↓
    Both access: sentinel_ai.db
```

### Multiple Machines
```
Chat Server (192.168.1.100:5000)
    ↓
    ├→ Chat Messages
    ├→ User Sessions
    ├→ Read Logs
    ↓
    sentinel_ai.db (shared)
    ↑
    ├→ Admin Analytics
    ├→ Threat Detection
    ├→ User Management
Admin Server (192.168.1.101:5000)
```

### Cloud/Docker (Swarm/Kubernetes)
```
LoadBalancer
    ├→ Chat Service   (replicas: 3)
    └→ Admin Service  (replicas: 1)
         ↓
    Shared PostgreSQL Database
```

---

## 📊 Admin Dashboard Features

When you access the admin panel:

### Statistics
- **Total Logs** - All audit events across users
- **Messages Today** - Message count from past 24 hours
- **Errors** - Failed API calls, exceptions
- **Server Status** - Health check indicator

### Activity Log Filters
```
All Actions
├── message_sent
├── login
├── logout
├── login_attempt
├── login_success
├── login_failure
├── threat             ← Brute-force, suspicious activity
├── api_error
└── fallback_response
```

### Real-Time Monitoring
- Auto-refresh every 30 seconds
- Search by user/IP/action
- Badge-based categorization
- Pagination for large datasets

---

## 🔑 Key Environment Variables

### Shared (Both Servers)
```bash
SECRET_KEY='your-secret-key'           # Must be identical
OPENAI_API_KEY='sk-...'                # API key(s)
DATABASE_URL='sqlite:///sentinel_ai.db' # (optional, if remote DB)
```

### Different Per Server
```bash
# Main Chat Server
(ADMIN_HOST not set)
FLASK_ENV='production'

# Admin Server
ADMIN_HOST='admin.localhost'      # Restrict to this host
FLASK_ENV='production'
# Optional: different port via CLI parameter --port 5001
```

---

## 🐛 Troubleshooting

### Issue: "Admin panel accessible only from admin host" (403)

**Your setup:**
- Main server on `localhost:5000` (ADMIN_HOST not set)
- Trying to access `/admin/dashboard` on same server
- Got 403 error

**Why? You didn't set ADMIN_HOST**

**Solution 1:** Access with local IP that matches
```powershell
# If ADMIN_HOST is not set, access should work from any host
# Try: http://localhost:5000/admin/dashboard
# If still fails: Check firewall/network ACLs
```

**Solution 2:** Set ADMIN_HOST correctly
```bash
# Terminal running admin server
export ADMIN_HOST='localhost'  # NOT 'localhost:5000'
python app.py --port 5001
```

---

### Issue: Token works on main server but not admin

**Cause:** Different `SECRET_KEY` on servers

**Fix:** Ensure both servers have IDENTICAL:
```bash
export SECRET_KEY='same-key-on-both-servers'
```

---

### Issue: Admin changes don't show on chat server

**Cause:** Different databases (unlikely with default config)

**Fix:** Verify DATABASE_URL is same:
```bash
# Both servers
export DATABASE_URL='sqlite:///sentinel_ai.db'
```

---

## 📈 Scaling Patterns

### Pattern 1: Small Team
```
1 Server with 2 Ports
├── :5000 Chat (users)
└── :5001 Admin Dashboard (internal-only)
```

### Pattern 2: Medium Deployment
```
2 Servers
├── Chat Server (:5000)
│   ├── users
│   ├── IDE
│   └── API
└── Admin Server (:5000 locally)
    ├── Analytics
    ├── Logs
    └── User Management
```

### Pattern 3: Enterprise
```
Load Balancer
├── Chat Cluster (3-5 replicas)
│   └── Shared PostgreSQL
├── Admin Cluster (1-2 replicas)
│   └── Same PostgreSQL
└── Cache Layer (Redis)
    └── Session data
```

---

## ✅ Implementation Checklist

- ✅ `ADMIN_HOST` environment variable support
- ✅ Host restriction logic in `/admin/dashboard` and `/admin/login`
- ✅ `require_admin` decorator implemented
- ✅ Database sharing across servers
- ✅ JWT token validation on both servers
- ✅ Admin dashboard link smart routing
- ✅ Threat logging & detection
- ✅ Forensic logs visible in admin panel
- ✅ Login attempt tracking
- ✅ Brute-force detection

---

## 🎓 Next Steps

1. **Test locally** with ADMIN_HOST configuration
2. **Deploy on separate ports** using Docker Compose example
3. **Configure DNS/hosts** for domain-based access
4. **Set up reverse proxy** (Nginx) for SSL/TLS
5. **Monitor both servers** with application insights
6. **Backup shared database** on regular schedule

---

## 📞 Support

For issues with admin host setup:
1. Check environment variables match between servers
2. Verify SECRET_KEY is identical
3. Confirm database file is accessible by both
4. Test JWT token flow
5. Check firewall/network ACLs

---

**Ready to deploy? Start with Tutorial 1 above!**
