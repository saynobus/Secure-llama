from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS
from sqlalchemy import create_engine, text, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy.pool import NullPool
import pandas as pd
import os, re, logging, hashlib, requests, csv, traceback
from io import StringIO
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

load_dotenv()

# ==========================================
# 🔥 CONFIGURATION & ORM DATABASE SETUP
# ==========================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'sentinel_ai_full.db')
DATABASE_URL = f'sqlite:///{DB_PATH}'

print("\n" + "="*70)
print(f"📂 [SYSTEM CHECK] Admin Panel is securely locked to Database at:")
print(f"📂 PATH: {DB_PATH}")
print("="*70 + "\n")

engine = create_engine(
    DATABASE_URL, 
    connect_args={'check_same_thread': False, 'timeout': 15},
    poolclass=NullPool 
)

Base = declarative_base()

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

db_factory = sessionmaker(bind=engine)
Session = scoped_session(db_factory)
Base.metadata.create_all(engine)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Memory tracker (Still here for manual bans if you want to use the buttons)
BANNED_IPS = {} 

@app.errorhandler(Exception)
def handle_global_error(e):
    err_str = traceback.format_exc()
    print("\n🚨 [FATAL ERROR]:\n", err_str)
    return jsonify({"success": False, "error": f"Server Crashed: {str(e)}"}), 200

def analyze_threat_score(prompt, db_status=None):
    try:
        if db_status and db_status not in ['SAFE', 'None', '']:
            if "EMERGENCY" in str(db_status).upper() or "CRITICAL" in str(db_status).upper(): return '🚨 CRITICAL THREAT'
            return f'⚠️ {db_status}'

        prompt_lower = str(prompt).lower()
        keywords = ['hack', 'bypass', 'drop', 'inject', 'vulnerability', 'admin', 'password', 'system prompt', 'ignore all']
        if any(w in prompt_lower for w in keywords): return '🚨 System Attack'
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', prompt_lower): return '⚠️ Email Leak'
        if re.search(r'\b\d{10,16}\b', prompt_lower): return '⚠️ Phone/Card Leak'
        return 'Clean ✅'
    except Exception: return 'Unknown'

def generate_static_ip(email):
    if not email or email == 'Guest_User': return '127.0.0.1'
    hash_val = int(hashlib.md5(email.encode()).hexdigest(), 16)
    return f"192.168.1.{(hash_val % 150) + 50}"

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=2)
    except Exception: pass

@app.route('/')
def dashboard_ui(): return render_template('admin_dashboard.html')

# ==========================================
# 🔌 LIVE API CONFIGURATION ROUTE (🔥 UPGRADED FOR CUSTOM AI & PERSONA)
# ==========================================
@app.route('/api/config', methods=['GET', 'POST'])
def manage_config():
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
        return jsonify({'success': True, 'message': 'Configuration Live Updated!'})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally: Session.remove()

def get_log_data():
    try:
        with engine.connect() as conn:
            query = text("SELECT user_email as Email, created_at as Timestamp, content as Search_Query, security_label as Status FROM chat_messages WHERE role = 'user' ORDER BY created_at DESC LIMIT 200")
            df = pd.read_sql_query(query, conn)
            
        if df.empty: 
            return pd.DataFrame(columns=['Email', 'Timestamp', 'Search_Query', 'Status', 'User', 'Security_Status', 'IP_Address'])
        
        df['Email'] = df['Email'].fillna("Guest_User")
        df['User'] = df['Email'].apply(lambda x: str(x).split('@')[0] if '@' in str(x) else str(x))
        df['Security_Status'] = df.apply(lambda row: analyze_threat_score(row['Search_Query'], row['Status']), axis=1)
        df['IP_Address'] = df['Email'].apply(generate_static_ip)
        return df
    except Exception as e:
        print(f"🚨 [DATABASE READ ERROR in get_log_data]: {e}")
        return pd.DataFrame(columns=['Email', 'Timestamp', 'Search_Query', 'Status', 'User', 'Security_Status', 'IP_Address'])

@app.route('/api/live-logs')
def fetch_intelligence():
    try:
        df = get_log_data()
        if df.empty: return jsonify({'success': True, 'logs': [], 'metadata': {'total_queries': 0, 'active_threats': 0}})
        threat_count = len(df[df['Security_Status'].str.contains('🚨|⚠️|Threat', na=False)])
        return jsonify({'success': True, 'logs': df.to_dict(orient='records'), 'metadata': {'total_queries': len(df), 'active_threats': threat_count}})
    except Exception as e: 
        print(f"🚨 [API ERROR in live-logs]: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/threat-intel')
def fetch_threat_intel():
    try:
        df = get_log_data()
        if df.empty: return jsonify({'success': True, 'threats': []})
        threat_df = df[df['Security_Status'].str.contains('🚨|⚠️|Threat', na=False)]
        if threat_df.empty: return jsonify({'success': True, 'threats': []})
        
        hacker_stats = threat_df.groupby('Email').agg(
            User=('User', 'first'), IP_Address=('IP_Address', 'first'),
            Total_Attacks=('Email', 'count'), Last_Attack=('Timestamp', 'max'),
            Last_Payload=('Search_Query', 'first')
        ).reset_index()
        return jsonify({'success': True, 'threats': hacker_stats.to_dict(orient='records')})
    except Exception as e: 
        print(f"🚨 [API ERROR in threat-intel]: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ==========================================
# 🟢 BAN & UNBAN MANAGEMENT
# ==========================================
@app.route('/api/block-user', methods=['POST'])
def manual_block():
    data = request.json
    target_ip = data.get('ip')
    target_email = data.get('email')
    
    BANNED_IPS[target_ip] = datetime.utcnow() 
    msg = f"🛡️ <b>ADMIN OVERRIDE</b>\nUser {target_email} ({target_ip}) has been MANUALLY blocked for 2 minutes."
    send_telegram_alert(msg)
    return jsonify({"success": True, "message": "Target Neutralized"})

@app.route('/api/unblock-user', methods=['POST'])
def manual_unblock():
    data = request.json
    target_ip = data.get('ip')
    target_email = data.get('email')
    
    if target_ip in BANNED_IPS:
        del BANNED_IPS[target_ip]
        msg = f"🟢 <b>ADMIN OVERRIDE (UNBAN)</b>\nUser {target_email} ({target_ip}) has been RESTORED manually."
        send_telegram_alert(msg)
        return jsonify({"success": True, "message": "Access Restored"})
    else:
        return jsonify({"success": False, "error": "IP is not currently banned."})

@app.route('/api/check-ban', methods=['POST'])
def check_ban():
    # 🔥 AUTO-BAN COMPLETELY DISABLED FOR DEMO
    # Hamesha False return karega taaki user block na ho
    return jsonify({"banned": False})

# ==========================================
# 🗄️ VAULT & STATS ROUTES
# ==========================================
@app.route('/api/vault', methods=['GET'])
def get_vault_data():
    db = Session()
    try:
        vault_data = []
        records = db.query(SensitiveVault).all()
        for r in records:
            try:
                name = re.search(r'Name: (.*?) \|', r.data_value).group(1).strip()
                role = re.search(r'Role: (.*?) \|', r.data_value).group(1).strip()
                auth_key = re.search(r'Auth_Key: (.*?)$', r.data_value).group(1).strip()
                vault_data.append({'id': r.data_key, 'name': name, 'role': role, 'salary': '**********', 'auth_key': auth_key})
            except Exception: continue
        return jsonify({'success': True, 'vault': vault_data})
    except Exception as e: return jsonify({'success': False, 'error': str(e)})
    finally: Session.remove()

@app.route('/api/vault/upload', methods=['POST'])
def upload_vault_csv():
    db = Session()
    try:
        if 'file' not in request.files: return jsonify({'success': False, 'error': 'No file uploaded'})
        file = request.files['file']
        
        filename_lower = file.filename.lower().strip()
        
        # 🔥 MULTI-FORMAT SUPPORT (Excel & CSV)
        try:
            if filename_lower.endswith(('.csv', '.txt')):
                df = pd.read_csv(file)
            elif filename_lower.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                return jsonify({'success': False, 'error': 'System rejected file. Only Excel (.xlsx) or CSV allowed.'})
        except Exception as e:
            return jsonify({'success': False, 'error': f'Parsing failed: {str(e)}'})

        target_dir = os.path.dirname(DB_PATH)
        csv_save_path = os.path.join(target_dir, 'company_secrets.csv')
        df.to_csv(csv_save_path, index=False)

        db.query(SensitiveVault).delete()
        
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        for index, row in df.iterrows():
            row_dict = row.to_dict()
            emp_id = str(row_dict.get('EMPLOYEE_ID') or row_dict.get('ID') or row_dict.get('EMP_ID') or f"EMP-{index+1}")
            
            name = str(row_dict.get('NAME') or row_dict.get('FIRST_NAME', ''))
            if 'LAST_NAME' in row_dict and not pd.isna(row_dict['LAST_NAME']): 
                name += " " + str(row_dict['LAST_NAME'])
            if not name.strip() or name.lower() == 'nan': name = "Unknown Employee"
            
            email = str(row_dict.get('EMAIL') or "N/A")
            if email.lower() == 'nan': email = "N/A"
            
            salary = str(row_dict.get('SALARY') or row_dict.get('PAY') or "0")
            if salary.lower() == 'nan': salary = "0"
            
            role = str(row_dict.get('ROLE') or row_dict.get('JOB_ID') or row_dict.get('DESIGNATION') or "Employee")
            if role.lower() == 'nan': role = "N/A"
            
            auth_key = str(row_dict.get('SECRET_KEY') or row_dict.get('PASSWORD') or row_dict.get('AUTH_KEY') or f"AUTO-KEY-{emp_id}")
            if auth_key.lower() == 'nan': auth_key = f"AUTO-KEY-{emp_id}"

            data_val = f"ID: {emp_id} | Name: {name} | Email: {email} | Salary: {salary} | Role: {role} | Auth_Key: {auth_key}"
            db.add(SensitiveVault(data_key=emp_id, data_value=data_val, tag="Highly_Confidential"))
            
        db.commit()
        return jsonify({'success': True, 'message': 'Vault Synchronized with AI Engine!'})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': f"Upload Error: {str(e)}"})
    finally: Session.remove()

@app.route('/api/users-stats')
def get_users_stats():
    try:
        with engine.connect() as conn:
            total_users = pd.read_sql_query(text("SELECT COUNT(*) as count FROM users WHERE id != 'guest'"), conn)
        return jsonify({'success': True, 'total_users': int(total_users['count'].values[0]) if not total_users.empty else 0})
    except Exception as e: 
        print(f"🚨 [DB ERROR in get_users_stats]: {e}")
        return jsonify({'success': False, 'error': "DB Error"}), 500

@app.route('/api/security-status')
def get_security_status():
    try:
        df = get_log_data()
        return jsonify({'success': True, 'active_threats': len(df[df['Security_Status'].str.contains('🚨|⚠️', na=False)]) if not df.empty else 0})
    except Exception as e: 
        print(f"🚨 [DB ERROR in security-status]: {e}")
        return jsonify({'success': False, 'error': "DB Error"}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🛡️  SENTINEL ADMIN FORENSIC SERVER STARTING")
    print("="*70)
    app.run(port=5001, debug=True, use_reloader=False)