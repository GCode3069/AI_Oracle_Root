#!/usr/bin/env python3
"""
SIMPLE MOBILE SERVER - No complex dependencies
Works offline with localStorage fallback
"""

from flask import Flask, send_file, request, jsonify
import json
import subprocess
from pathlib import Path
from datetime import datetime

app = Flask(__name__, static_folder='.')

BASE = Path("F:/AI_Oracle_Root/scarify")
QUEUE_FILE = BASE / "mobile_queue.json"
IDEAS_FILE = BASE / "mobile_ideas.json"

@app.route('/')
def home():
    """Serve mobile interface"""
    return send_file('MOBILE_SIMPLE.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """Start generation"""
    style = request.args.get('style', 'chatgpt')
    count = int(request.args.get('count', 5))
    
    job_id = f"MOB_{datetime.now().strftime('%H%M%S')}"
    
    # Save to queue
    queue = []
    if QUEUE_FILE.exists():
        queue = json.loads(QUEUE_FILE.read_text())
    
    queue.append({
        'id': job_id,
        'style': style,
        'count': count,
        'time': datetime.now().isoformat(),
        'status': 'queued'
    })
    
    QUEUE_FILE.write_text(json.dumps(queue, indent=2))
    
    # Start generation (async)
    def gen():
        subprocess.run(
            f'python BATCH_MIXED_STRATEGY.py {count} --start 70000',
            shell=True, cwd=str(BASE)
        )
    
    import threading
    threading.Thread(target=gen, daemon=True).start()
    
    return jsonify({'job_id': job_id, 'success': True})

@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get stats"""
    uploaded = BASE / "abraham_horror" / "uploaded"
    total = len(list(uploaded.glob("*.mp4"))) if uploaded.exists() else 0
    
    queued = 0
    if QUEUE_FILE.exists():
        queue = json.loads(QUEUE_FILE.read_text())
        queued = sum(1 for q in queue if q.get('status') == 'queued')
    
    return jsonify({
        'total': total,
        'queued': queued,
        'revenue': total * 5  # $5 estimate per video
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  📱 MOBILE SERVER - SIMPLE MODE")
    print("="*60)
    
    # Get IP
    import socket
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    
    print(f"\n  ON YOUR iPHONE:")
    print(f"  Open Safari → http://{ip}:5000")
    print(f"\n" + "="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)


