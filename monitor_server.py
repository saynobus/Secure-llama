from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import logging

# Disable default flask logging to keep terminal clean
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
CORS(app)
# async_mode='threading' is best for Windows stability
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

@app.route('/')
@app.route('/inspect/<email>')
def monitor_ui(email="GLOBAL"):
    """Renders the Live Simulation Dashboard"""
    return render_template('monitor.html', target_email=email)

@app.route('/bridge', methods=['POST'])
def bridge():
    """Receives data from app.py (Port 5000) and sends it to the UI"""
    packet_data = request.json
    socketio.emit('packet_trace', packet_data)
    return jsonify({"status": "Success", "message": "Packet relayed to SOC"}), 200

if __name__ == '__main__':
    print("=====================================================")
    print(" 🛰️ SENTINEL SOC MONITOR ACTIVE ON http://127.0.0.1:5002")
    print("=====================================================")
    socketio.run(app, host='0.0.0.0', port=5002, debug=True)