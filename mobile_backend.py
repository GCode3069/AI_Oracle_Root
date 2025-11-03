#!/usr/bin/env python3
"""
MOBILE BACKEND - Flask API for iPhone generator
Allows remote video generation via mobile interface
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import subprocess
import threading
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from mobile

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
IDEAS_FILE = BASE_DIR / "mobile_ideas.json"
JOBS_FILE = BASE_DIR / "mobile_jobs.json"

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """Serve the mobile HTML interface"""
    return app.send_static_file('MOBILE_GENERATOR.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Start video generation from mobile"""
    data = request.json
    
    style = data.get('style', 'chatgpt_poetic')
    ctr_level = data.get('ctr_level', 'moderate')
    count = data.get('count', 5)
    
    # Create job ID
    job_id = f"MOB_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Start generation in background
    def run_generation():
        try:
            # Use mixed batch generator
            cmd = f'python BATCH_MIXED_STRATEGY.py {count} --start 70000'
            
            # Or use production pipeline if specific style
            # cmd = f'python abraham_MAX_HEADROOM.py {count}'
            
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=str(BASE_DIR),
                capture_output=True,
                text=True
            )
            
            # Log result
            log_job(job_id, 'complete', result.returncode)
            
        except Exception as e:
            log_job(job_id, 'failed', str(e))
    
    # Start in background thread
    thread = threading.Thread(target=run_generation)
    thread.daemon = True
    thread.start()
    
    # Log job
    log_job(job_id, 'started', {
        'style': style,
        'ctr': ctr_level,
        'count': count
    })
    
    estimated_time = count * 3  # 3 minutes per video estimate
    
    return jsonify({
        'success': True,
        'job_id': job_id,
        'videos': count,
        'estimated_time': estimated_time,
        'message': f'Generating {count} videos in background'
    })

@app.route('/save_idea', methods=['POST'])
def save_idea():
    """Save idea for later generation"""
    data = request.json
    
    idea = data.get('idea', '')
    if not idea:
        return jsonify({'success': False, 'error': 'No idea provided'}), 400
    
    # Load existing ideas
    if IDEAS_FILE.exists():
        with open(IDEAS_FILE, 'r', encoding='utf-8') as f:
            ideas = json.load(f)
    else:
        ideas = []
    
    # Add new idea
    ideas.append({
        'idea': idea,
        'timestamp': data.get('timestamp', datetime.utcnow().isoformat() + 'Z'),
        'status': 'pending'
    })
    
    # Save
    with open(IDEAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(ideas, f, indent=2)
    
    return jsonify({
        'success': True,
        'total_ideas': len(ideas),
        'message': 'Idea saved successfully'
    })

@app.route('/stats', methods=['GET'])
def stats():
    """Get current stats for mobile display"""
    
    # Count videos
    uploaded_dir = BASE_DIR / "abraham_horror" / "uploaded"
    if uploaded_dir.exists():
        total_videos = len(list(uploaded_dir.glob("*.mp4")))
    else:
        total_videos = 0
    
    # Count queued jobs
    queued = 0
    if JOBS_FILE.exists():
        with open(JOBS_FILE, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
            queued = sum(1 for j in jobs if j.get('status') == 'started')
    
    # Estimate revenue (rough)
    revenue = total_videos * 5  # $5 average per video estimate
    
    return jsonify({
        'total_videos': total_videos,
        'queued': queued,
        'revenue': revenue,
        'last_updated': datetime.utcnow().isoformat() + 'Z'
    })

@app.route('/ideas', methods=['GET'])
def get_ideas():
    """Get all saved ideas"""
    if IDEAS_FILE.exists():
        with open(IDEAS_FILE, 'r', encoding='utf-8') as f:
            ideas = json.load(f)
        return jsonify({'ideas': ideas})
    else:
        return jsonify({'ideas': []})

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def log_job(job_id, status, details=None):
    """Log job to jobs file"""
    if JOBS_FILE.exists():
        with open(JOBS_FILE, 'r', encoding='utf-8') as f:
            jobs = json.load(f)
    else:
        jobs = []
    
    # Find existing job or create new
    job = next((j for j in jobs if j['id'] == job_id), None)
    if job:
        job['status'] = status
        job['updated_at'] = datetime.utcnow().isoformat() + 'Z'
        if details:
            job['details'] = details
    else:
        jobs.append({
            'id': job_id,
            'status': status,
            'created_at': datetime.utcnow().isoformat() + 'Z',
            'details': details
        })
    
    with open(JOBS_FILE, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*80)
    print("  📱 MOBILE BACKEND SERVER")
    print("="*80 + "\n")
    print("Starting Flask server...")
    print("\nAccess from iPhone:")
    print("  1. Find your PC's IP address (ipconfig)")
    print("  2. Open Safari on iPhone")
    print("  3. Go to: http://YOUR_PC_IP:5000")
    print("\nExample: http://192.168.1.100:5000")
    print("\nServer starting on port 5000...")
    print("\n" + "="*80 + "\n")
    
    # Run server (accessible from local network)
    app.run(host='0.0.0.0', port=5000, debug=True)


