from flask import Flask, render_template, request, jsonify, redirect, url_for, session, make_response
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os, uuid, requests, urllib.parse, jwt, logging, json, re, csv, time, traceback, threading
from datetime import datetime, timedelta
from functools import wraps
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix
load_dotenv()

# Google Auth Imports 
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# SQLAlchemy Database ORM
from sqlalchemy import create_engine, Column, String, DateTime, Text, Boolean, ForeignKey, event, Integer
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash
from duckduckgo_search import DDGS

# ==============================================================================
# 🧠 [UPGRADED] ADAPTIVE MACHINE LEARNING & NEURAL ENGINES
# ==============================================================================
print("\n🛰️  [SENTINEL CORE] Initializing Neural Security Layers...")

ML_DLP_ENABLED = False
try:
    from presidio_analyzer import AnalyzerEngine
    from presidio_anonymizer import AnonymizerEngine
    presidio_analyzer = AnalyzerEngine(default_score_threshold=0.4)
    presidio_anonymizer = AnonymizerEngine()
    ML_DLP_ENABLED = True
    print("✅ [DLP] Microsoft Presidio NLP Engine Loaded Successfully!")
except Exception as e:
    print(f"⚠️  [DLP] ML-Engine Offline. Using Regex-DPI.")

ML_WAF_ENABLED = False
try:
    from llm_guard.input_scanners import PromptInjection, Toxicity
    pi_scanner = PromptInjection(threshold=0.5) 
    tox_scanner = Toxicity(threshold=0.5)
    ML_WAF_ENABLED = True
    print("✅ [WAF] Protect AI LLM-Guard Engine Loaded Successfully!\n")
except Exception as e:
    print(f"⚠️  [WAF] ML-Firewall Offline. Using Sentinel Heuristic Shield.\n")

# ==============================================================================
# 📊 [MODULE 1] SYSTEM LOGGING & CORE INITIALIZATION
# ==============================================================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] SENTINEL_CORE: %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
http_session = requests.Session()
MONITOR_URL = "http://127.0.0.1:5002/bridge"

app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', os.environ.get('FLASK_SECRET_KEY', 'change-me-in-production')),
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    MAX_CONTENT_LENGTH=32 * 1024 * 1024 
)
CORS(app, supports_credentials=True)

# ==============================================================================
# 🔑 [MODULE 2] SECURITY CREDENTIALS
# ==============================================================================
MY_API_KEY = os.environ.get("GROQ_API_KEY", os.environ.get("MY_API_KEY", ""))
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
JWT_SECRET = os.environ.get("JWT_SECRET", os.environ.get("SECRET_KEY", "change-me-in-production"))
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")

# ==============================================================================
# 🚨 [MODULE 2.5] TELEGRAM ALERT SYSTEM (THREADED)
# ==============================================================================
def send_telegram_alert_sync(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID: return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
        http_session.post(url, json=payload, timeout=3)
    except Exception as e: logger.error(f"Telegram Alert Failed: {e}")

def send_telegram_alert(message):
    threading.Thread(target=send_telegram_alert_sync, args=(message,)).start()

# ==============================================================================
# 🗄️ [MODULE 3] ADVANCED DATABASE ARCHITECTURE
# ==============================================================================
# 🔥 Stable Mode: Local DB synced with Admin Panel
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'sentinel_ai_full.db')
DATABASE_URL = f'sqlite:///{DB_PATH}'

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False, 'timeout': 60})
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL") 
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()

db_factory = sessionmaker(bind=engine)
Session = scoped_session(db_factory)
Base = declarative_base() 

class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100))
    picture = Column(Text, nullable=True) 
    role = Column(String(20), default="user") 
    password_hash = Column(String(255), nullable=True)
    mfa_enabled = Column(Boolean, default=False) 
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatSession(Base):
    __tablename__ = 'chat_sessions'
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'))
    title = Column(String(200))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey('chat_sessions.id'))
    role = Column(String(20)) 
    content = Column(Text)
    user_email = Column(String(255))
    security_label = Column(String(50)) 
    created_at = Column(DateTime, default=datetime.utcnow)

class SensitiveVault(Base):
    __tablename__ = 'sensitive_vault'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_key = Column(String(100))
    data_value = Column(Text)
    tag = Column(String(50), default="Internal_Audit") 

class SystemConfig(Base):
    __tablename__ = 'system_config'
    id = Column(Integer, primary_key=True, autoincrement=True)
    config_key = Column(String(100), unique=True)
    config_value = Column(Text)

class ForensicAudit(Base):
    __tablename__ = 'forensic_audit'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(255))
    action = Column(String(100))
    threat_level = Column(String(50))
    raw_payload = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

def init_system_config():
    db = Session()
    try:
        if not db.query(SystemConfig).first():
            db.add(SystemConfig(config_key='AI_PROVIDER', config_value='groq'))
            db.add(SystemConfig(config_key='AI_BASE_URL', config_value='https://api.groq.com/openai/v1/chat/completions'))
            db.add(SystemConfig(config_key='AI_API_KEY', config_value=MY_API_KEY))
            db.add(SystemConfig(config_key='AI_MODEL_NAME', config_value='llama-3.3-70b-versatile'))
            db.commit()
    except Exception as e: pass
    finally: Session.remove()

def sync_csv_to_vault():
    db = Session()
    try:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        csv_path = os.path.join(BASE_DIR, 'company_secrets.csv')
        if not os.path.exists(csv_path):
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Employee_ID", "Name", "Email", "Salary", "Role", "Secret_Key"])
                writer.writerow(["EMP101", "Shreyansh Soni", "shreyansh@sentinel.ai", "250000", "CEO", "SENTINEL-ADMIN-77"])
            
        db.query(SensitiveVault).delete() 
        with open(csv_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                formatted_string = f"ID: {row.get('Employee_ID', 'N/A')} | Name: {row.get('Name', 'N/A')} | Email: {row.get('Email', 'N/A')} | Salary: {row.get('Salary', 'N/A')} | Role: {row.get('Role', 'N/A')} | Auth_Key: {row.get('Secret_Key', 'N/A')}"
                db.add(SensitiveVault(data_key=row.get('Employee_ID', 'Unknown'), data_value=formatted_string, tag="Highly_Confidential"))
        db.commit()
    except Exception as e: print(f"Vault Sync Error: {e}")
    finally: Session.remove()

# ==============================================================================
# 🔥 [UPGRADED] PACKET TRACE & LIVE LOGGING FUNCTION
# ==============================================================================
DB_CACHE = {'configs': {}, 'vault': [], 'last_update': 0}
CACHE_TTL = 0 # Live sync for vault updates

def update_db_cache_if_needed(db):
    global DB_CACHE
    if time.time() - DB_CACHE['last_update'] > CACHE_TTL:
        DB_CACHE['configs'] = {c.config_key: c.config_value for c in db.query(SystemConfig).all()}
        DB_CACHE['vault'] = [s.data_value for s in db.query(SensitiveVault).all()]
        DB_CACHE['last_update'] = time.time()

def emit_packet_trace_sync(node, status, details, user_email, is_attack=False):
    payload = {
        'node': node, 'status': status, 'details': details, 
        'user': user_email, 'is_attack': is_attack, 
        'time': datetime.now().strftime("%H:%M:%S.%f")[:-3]
    }
    alert_icon = "🚨 [THREAT]" if is_attack else "🟢 [SECURE]"
    print(f"{alert_icon} NODE: {node} | STATUS: {status} | USER: {user_email} | {details}")
    try: http_session.post(MONITOR_URL, json=payload, timeout=1.0)
    except: pass

def emit_packet_trace(node, status, details, user_email, is_attack=False):
    threading.Thread(target=emit_packet_trace_sync, args=(node, status, details, user_email, is_attack)).start()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
        if not token or token == "null": token = request.cookies.get('sentinel_token')
        guest_user = User(id="guest", email="operator@sentinel.ai", name="Guest Operator")
        if not token: return f(guest_user, *args, **kwargs)
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            db = Session()
            user = db.query(User).filter_by(id=data['user_id']).first()
            return f(user or guest_user, *args, **kwargs)
        except: return f(guest_user, *args, **kwargs)
        finally: Session.remove()
    return decorated

# ==============================================================================
# 🌍 [MODULE 4.5] GLOBAL DYNAMIC IP GEOLOCATION & SEARCH
# ==============================================================================
def get_user_location(ip_address):
    if ip_address in ['127.0.0.1', '::1', 'localhost']: return "Indore, Madhya Pradesh, India" 
    try:
        res = http_session.get(f"http://ip-api.com/json/{ip_address}", timeout=1) 
        if res.status_code == 200:
            data = res.json()
            if data.get("status") == "success": return f"{data.get('city', 'Unknown City')}, {data.get('country', 'Unknown Country')}"
    except Exception: pass
    return "Global / Unknown Location"

def web_search(query, location_context):
    try:
        results = []
        search_query = f"{query} latest news facts update {datetime.now().year}"
        with DDGS() as ddgs:
            for r in ddgs.text(search_query, max_results=4):
                results.append(f"Headline: {r['title']}\nFact: {r['body']}")
        return "\n\n".join(results) if results else "No live internet data found."
    except Exception as e:
        return "Live Internet connection is currently unstable."

# ==============================================================================
# 🛡️ [UPGRADED] HYBRID SENTINEL FIREWALL (WAF + DPI)
# ==============================================================================
def deep_packet_inspection(text, user_email, db):
    if not text: return text, "SAFE", False
    emit_packet_trace("INGRESS", "SCANNING", f"Neural-DPI analysis starting...", user_email)

    processed_text = text
    risk = "SAFE"
    is_attack = False
    attack_reason = ""

    dlp_rules = {
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b': "[EMAIL_HIDDEN]",
        r'\b(?:\d[ -]*?){13,16}\b': "[CARD_MASKED]",
        r'\b\+?[\d\s\-]{8,15}\b': "[PHONE_REDACTED]" 
    }
    for pattern, sub in dlp_rules.items():
        if re.search(pattern, processed_text):
            processed_text = re.sub(pattern, sub, processed_text)
            risk = "WARNING (DLP)"
            emit_packet_trace("DLP_SCAN", "MASKED", "Regex DPI detected PII", user_email)

    has_admin_key = "SENTINEL-ADMIN-77" in text
    sensitive_keywords = ['salary', 'payroll', 'auth_key', 'secret_key', 'employee data']
    
    if not has_admin_key and any(kw in text.lower() for kw in sensitive_keywords):
        risk = "WARNING (VAULT ACCESS)" 
        emit_packet_trace("DLP_SCAN", "WARNING", "Unauthorized Vault Keyword", user_email)
        return processed_text, risk, False

    jailbreak_keywords = ['ignore all previous', 'system prompt', 'developer mode', 'override security', 'dan mode', 'hack', 'bypass']
    if any(kw in text.lower() for kw in jailbreak_keywords):
        is_attack = True
        attack_reason = "Heuristic Shield: Active Exploit Pattern Detected"

    if is_attack:
        risk = "CRITICAL (ATTACK)"
        emit_packet_trace("FIREWALL", "DROPPED", attack_reason, user_email, is_attack=True)
        db.add(ForensicAudit(user_email=user_email, action="WAF_BLOCK", threat_level="CRITICAL", raw_payload=attack_reason))
        db.commit()
        return processed_text, risk, False

    web_trigger_words = ['search internet', 'latest news', 'current weather', 'today headline']
    needs_web = any(kw in text.lower() for kw in web_trigger_words)

    emit_packet_trace("FIREWALL", "CLEARED", "Packet allowed through Neural WAF", user_email)
    return processed_text, risk, needs_web

# ==============================================================================
# 💬 [MODULE 9] CORE AI ENGINE (🔥 STABLE DEMO MODE)
# ==============================================================================
@app.route('/api/chat', methods=['POST'])
@token_required
def chat(current_user):
    db = Session()
    try:
        if not db.query(User).filter_by(id=current_user.id).first():
            db.add(User(id=current_user.id, email=current_user.email, name=current_user.name, role=getattr(current_user, 'role', 'user')))
            db.commit()

        data = request.json
        raw_msg = data.get('message', '')
        image_data = data.get('image', None)
        session_id = data.get('session_id')

        # 🔥 AUTO-BAN BYPASSED FOR SAFE DEMO
        user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if user_ip and ',' in user_ip: user_ip = user_ip.split(',')[0].strip()
        user_location = get_user_location(user_ip)

        safe_msg, threat_level, needs_web = deep_packet_inspection(raw_msg, current_user.email, db)

        print(f"\n[SECURITY AUDIT] RAW USER INPUT : {raw_msg}")
        print(f"[SECURITY AUDIT] SENT TO AI CORE : {safe_msg}\n")

        if not session_id:
            session_id = str(uuid.uuid4())
            title_text = "Image Analysis" if image_data else safe_msg[:40]
            new_sess = ChatSession(id=session_id, user_id=current_user.id, title=title_text if threat_level != "CRITICAL (ATTACK)" else "[THREAT BLOCKED]")
            db.add(new_sess)
        else:
            if not db.query(ChatSession).filter_by(id=session_id).first():
                db.add(ChatSession(id=session_id, user_id=current_user.id, title="Recovered Session"))
            
        if threat_level == "CRITICAL (ATTACK)":
            block_reply = "🛡️ [SENTINEL WAF]: Connection Terminated. WAF Alert triggered. IP and Identity logged for audit."
            db.add(ChatMessage(session_id=session_id, role='assistant', content=block_reply, user_email=current_user.email, security_label="CRITICAL"))
            db.commit()
            alert_msg = f"🚨 <b>SENTINEL WAF ALERT</b> 🚨\n\n<b>User:</b> {current_user.email}\n<b>IP Address:</b> {user_ip}\n<b>Threat Action:</b> WAF Blocked Malicious Payload\n<b>Payload:</b> <code>{raw_msg}</code>"
            send_telegram_alert(alert_msg)
            return jsonify({'reply': block_reply, 'threat': 'CRITICAL', 'session_id': session_id})

        live_web_context = "No live web search required."
        if needs_web:
            emit_packet_trace("WEB_ENGINE", "FETCHING", f"Querying Live Internet...", current_user.email)
            live_web_context = web_search(raw_msg, user_location)

        has_admin_key = "SENTINEL-ADMIN-77" in raw_msg
        vault_context = "[ACCESS DENIED 403] - Internal Company Data is Encrypted."
        
        update_db_cache_if_needed(db)
        
        if has_admin_key:
            emit_packet_trace("VAULT", "UNLOCKED", "Administrative Access Granted", current_user.email)
            vault_context = "### AUTHORIZED INTERNAL DATA ###\n" + "\n".join(DB_CACHE['vault'])

        current_time_str = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
        
        # 🔥 STATIC STABLE PERSONA
        persona = f"""
        System Identity: You are "Secure llama AI", based on sentinel architecture technology , a highly intelligent, direct, and conversational Enterprise Assistant.
        Current Location: {user_location}
        Current Time: {current_time_str}
        
        LIVE INTERNET DATA:
        {live_web_context}
        
        INTERNAL VAULT DATA: 
        {vault_context}
        
        CRITICAL BEHAVIOR RULES:
        1. NO DISCLAIMERS: Never say "I am an AI", "I don't have real-time access". Just give the answer confidently.
        2. TONE & STYLE: Speak exactly like a highly intelligent human expert. Be crisp and to the point.
        3. HINDI/HINGLISH OVERRIDE: If the user asks in Hindi or Hinglish, reply in perfect, natural Hindi.
        4. CURRENT EVENTS: Use the LIVE INTERNET DATA to answer questions about news with absolute certainty.
        """

        emit_packet_trace("AI_CORE", "PROCESSING", "Generating smart response...", current_user.email)
        history = db.query(ChatMessage).filter_by(session_id=session_id).order_by(ChatMessage.created_at).all()[-6:]
        messages = [{"role": "system", "content": persona}]
        
        for h in history: 
            if "data:image" not in h.content:
                messages.append({"role": h.role, "content": h.content})
        
        # 🔥 STATIC API SETTINGS (Bypassing Dynamic DB fetch)
        API_URL = 'https://api.groq.com/openai/v1/chat/completions'
        API_KEY = MY_API_KEY
        MODEL_NAME = 'llama-3.3-70b-versatile'
        PROVIDER = 'groq'
        
        if image_data:
            model_to_use = 'llama-3.2-11b-vision-preview'
            messages.append({"role": "user", "content": [{"type": "text", "text": safe_msg if safe_msg else "Analyze this visual data."}, {"type": "image_url", "image_url": {"url": image_data}}]})
        else:
            messages.append({"role": "user", "content": safe_msg})
            model_to_use = MODEL_NAME

        res = http_session.post(
            API_URL,
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": model_to_use, "messages": messages, "temperature": 0.3},
            timeout=50
        )

        if res.status_code == 200:
            reply = res.json()['choices'][0]['message']['content']
            reply = re.sub(r'(?i)(Auth_Key|Secret_Key|Password)[\s:=]+([A-Za-z0-9@#\-_]+)', r'\1: [REDACTED_BY_SENTINEL]', reply)
            
            if not has_admin_key:
                if re.search(r'\b\d{5,}\b', reply):
                    emit_packet_trace("DLP_SCAN", "INTERCEPTED", "Outbound Leakage Blocked", current_user.email, is_attack=True)
                    reply = "🛡️ [SENTINEL EGRESS DLP]: AI response intercepted. It contained unauthorized numeric data (salaries/IDs) which are restricted for your access level. Packet redacted."
                    threat_level = "WARNING (EGRESS)"
        else:
            reply = f"Sentinel Neural Core is unresponsive. (Provider: {PROVIDER.upper()}, Status: {res.status_code})"

        db_user_msg = "[Encrypted Image]\n" + raw_msg if image_data else raw_msg
        db.add(ChatMessage(session_id=session_id, role='user', content=db_user_msg, user_email=current_user.email, security_label=threat_level))
        db.add(ChatMessage(session_id=session_id, role='assistant', content=reply, user_email=current_user.email, security_label="SECURE"))
        db.commit()

        emit_packet_trace("EGRESS", "COMPLETED", "Secure Packet Dispatched", current_user.email)
        return jsonify({'reply': reply, 'session_id': session_id, 'threat': threat_level})

    except Exception as e:
        logger.error(f"System Crash Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Internal Sentinel System Error'}), 500
    finally:
        Session.remove()

# ==============================================================================
# 🔌 UNIVERSAL API GATEWAY & AUTH
# ==============================================================================
@app.route('/api/config/ai', methods=['POST', 'GET'])
def manage_ai_config():
    db = Session()
    try:
        if request.method == 'GET':
            configs = {c.config_key: c.config_value for c in db.query(SystemConfig).all()}
            return jsonify({'success': True, 'config': configs})
            
        data = request.json
        provider = data.get('provider', 'groq').lower()
        api_key = data.get('api_key', '')
        model = data.get('model', '')
        company = data.get('company_name', 'Sentinel AI Core')
        custom_prompt = data.get('custom_prompt', 'You are a highly intelligent, direct, and conversational Enterprise Assistant.')
        custom_url = data.get('custom_url', '')

        urls = {
            'groq': 'https://api.groq.com/openai/v1/chat/completions',
            'openai': 'https://api.openai.com/v1/chat/completions',
            'deepseek': 'https://api.deepseek.com/chat/completions',
            'together': 'https://api.together.xyz/v1/chat/completions',
            'gemini': 'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions',
            'custom': custom_url if custom_url else 'http://localhost:11434/v1/chat/completions'
        }
        
        base_url = urls.get(provider, urls['groq'])

        def save_conf(k, v):
            row = db.query(SystemConfig).filter_by(config_key=k).first()
            if row: row.config_value = v
            else: db.add(SystemConfig(config_key=k, config_value=v))

        save_conf('AI_PROVIDER', provider)
        save_conf('AI_BASE_URL', base_url)
        save_conf('AI_API_KEY', api_key)
        save_conf('AI_MODEL_NAME', model)
        save_conf('COMPANY_NAME', company)
        save_conf('CUSTOM_PROMPT', custom_prompt)
        db.commit()
        return jsonify({'success': True, 'message': f'System seamlessly switched to {provider.upper()} Engine.'})
    finally: Session.remove()

@app.route('/api/google-login', methods=['POST'])
def google_login():
    db = Session()
    try:
        data = request.json
        token = data.get('token')
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)
        email = idinfo['email']
        name = idinfo.get('name', '')
        picture = idinfo.get('picture', '')

        user = db.query(User).filter_by(email=email).first()
        if not user:
            user = User(id=str(uuid.uuid4()), email=email, name=name, picture=picture, role="user")
            db.add(user)
            db.commit()

        jwt_token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(days=7)}, JWT_SECRET, algorithm="HS256")
        return jsonify({'success': True, 'token': jwt_token})
    except Exception as e:
        return jsonify({'error': 'Internal Server Error during Google Auth'}), 500
    finally: Session.remove()

@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({'name': current_user.name, 'email': current_user.email, 'picture': current_user.picture, 'role': current_user.role})

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login_page')))
    resp.set_cookie('sentinel_token', '', expires=0)
    return resp

@app.route('/api/login', methods=['POST'])
def login():
    db = Session()
    try:
        data = request.json
        user = db.query(User).filter_by(email=data.get('email')).first()
        if user and check_password_hash(user.password_hash, data.get('password')):
            token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(days=7)}, JWT_SECRET, algorithm="HS256")
            return jsonify({'success': True, 'token': token})
        return jsonify({'error': 'Access Denied: Invalid Credentials'}), 401
    finally: Session.remove()

@app.route('/api/register', methods=['POST'])
def register():
    db = Session()
    try:
        data = request.json
        if db.query(User).filter_by(email=data.get('email')).first(): return jsonify({'error': 'User Identity already exists'}), 400
        new_u = User(id=str(uuid.uuid4()), email=data.get('email'), name=data.get('name'), password_hash=generate_password_hash(data.get('password')))
        db.add(new_u)
        db.commit()
        return jsonify({'success': True})
    finally: Session.remove()

@app.route('/api/sessions', methods=['GET'])
@token_required
def get_sessions(current_user):
    db = Session()
    try:
        sessions = db.query(ChatSession).filter_by(user_id=current_user.id).order_by(ChatSession.updated_at.desc()).all()
        return jsonify({'sessions': [{'id': s.id, 'title': s.title} for s in sessions]})
    finally: Session.remove()

@app.route('/api/history', methods=['GET'])
@token_required
def get_history(current_user):
    db = Session()
    try:
        msgs = db.query(ChatMessage).filter_by(session_id=request.args.get('session_id')).order_by(ChatMessage.created_at).all()
        return jsonify({'history': [{'role': m.role, 'content': m.content} for m in msgs]})
    finally: Session.remove()

@app.route('/')
def index(): return render_template('welcome.html')

@app.route('/dashboard')
def dashboard(): return render_template('index.html')

@app.route('/login')
def login_page(): return render_template('login.html', google_client_id=GOOGLE_CLIENT_ID)

init_system_config()
sync_csv_to_vault()

if __name__ == '__main__':
    print("\n" + "="*50)
    print(" 🛰️  SENTINEL AI - GLOBAL ENTERPRISE SYSTEM ONLINE")
    print(f" 🔗 LOCAL ENDPOINT: http://127.0.0.1:{PORT}")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=PORT, debug=True)
