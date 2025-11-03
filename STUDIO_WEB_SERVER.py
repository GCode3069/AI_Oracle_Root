#!/usr/bin/env python3
"""
ABRAHAM STUDIO - Web Server for iPhone Access
Flask-based web interface to control studio from mobile
"""
import os
import sys
import json
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, send_file
from flask_cors import CORS

# Add parent directory to path
BASE = Path("F:/AI_Oracle_Root/scarify")
sys.path.insert(0, str(BASE))

app = Flask(__name__)
CORS(app)  # Enable cross-origin for mobile access

STUDIO_DIR = BASE / "abraham_studio"
STUDIO_SCRIPT = BASE / "ABRAHAM_STUDIO (1).pyw"

# Generation status
generation_status = {
    'running': False,
    'progress': 0,
    'total': 0,
    'current_video': 0,
    'log': [],
    'results': []
}

# ============================================================================
# HTML TEMPLATE (Mobile-friendly)
# ============================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ABRAHAM STUDIO - Mobile Control</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: #1a0000;
            color: white;
            padding: 20px;
        }
        .container { max-width: 600px; margin: 0 auto; }
        h1 {
            color: #ff0000;
            text-align: center;
            margin-bottom: 30px;
            font-size: 24px;
        }
        .card {
            background: #2a0000;
            border: 1px solid #440000;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #ff6666;
            font-weight: bold;
        }
        select, input[type="number"], input[type="checkbox"] {
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
            background: #1a0000;
            border: 1px solid #440000;
            color: white;
            border-radius: 5px;
            font-size: 16px;
        }
        .checkbox-container {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        .checkbox-container input[type="checkbox"] {
            width: auto;
            margin-right: 10px;
            margin-bottom: 0;
        }
        button {
            width: 100%;
            padding: 15px;
            background: #ff0000;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            margin-bottom: 10px;
        }
        button:disabled {
            background: #666;
            cursor: not-allowed;
        }
        .status {
            background: #0a0000;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            max-height: 300px;
            overflow-y: auto;
        }
        .log-entry {
            margin: 5px 0;
            color: #00ff00;
        }
        .error { color: #ff6666; }
        .progress-bar {
            width: 100%;
            height: 30px;
            background: #1a0000;
            border: 1px solid #440000;
            border-radius: 5px;
            margin: 10px 0;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: #ff0000;
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🩸 ABRAHAM STUDIO</h1>
        
        <div class="card">
            <form id="generateForm">
                <label>Region:</label>
                <select id="region" name="region">
                    <option value="USA (National)">USA (National)</option>
                    <option value="USA - Texas">USA - Texas</option>
                    <option value="USA - California">USA - California</option>
                    <option value="USA - New York">USA - New York</option>
                    <option value="USA - Florida">USA - Florida</option>
                    <option value="Spain">Spain</option>
                    <option value="Mexico">Mexico</option>
                    <option value="United Kingdom">United Kingdom</option>
                    <option value="Brazil">Brazil</option>
                    <option value="Germany">Germany</option>
                </select>
                
                <label>Number of Videos:</label>
                <input type="number" id="count" name="count" min="1" max="50" value="5">
                
                <label>Engine:</label>
                <select id="engine" name="engine">
                    <option value="stability">Stability AI</option>
                    <option value="pollo">Pollo AI</option>
                    <option value="both">Both</option>
                </select>
                
                <div class="checkbox-container">
                    <input type="checkbox" id="adult" name="adult">
                    <label for="adult" style="margin:0;">🩸 Adult Gore Mode</label>
                </div>
                
                <button type="submit" id="generateBtn">🚀 GENERATE VIDEOS</button>
            </form>
        </div>
        
        <div class="card">
            <h2>Status</h2>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill" style="width: 0%;">0%</div>
            </div>
            <div id="statusText">Ready</div>
            
            <div class="status" id="log">
                <div class="log-entry">Waiting for generation...</div>
            </div>
        </div>
    </div>
    
    <script>
        const form = document.getElementById('generateForm');
        const generateBtn = document.getElementById('generateBtn');
        const log = document.getElementById('log');
        const progressFill = document.getElementById('progressFill');
        const statusText = document.getElementById('statusText');
        
        let pollingInterval = null;
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = {
                region: document.getElementById('region').value,
                count: parseInt(document.getElementById('count').value),
                engine: document.getElementById('engine').value,
                adult: document.getElementById('adult').checked
            };
            
            generateBtn.disabled = true;
            generateBtn.textContent = 'Generating...';
            log.innerHTML = '<div class="log-entry">Starting generation...</div>';
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(formData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    startPolling();
                } else {
                    alert('Error: ' + data.error);
                    generateBtn.disabled = false;
                    generateBtn.textContent = '🚀 GENERATE VIDEOS';
                }
            } catch (error) {
                alert('Error: ' + error.message);
                generateBtn.disabled = false;
                generateBtn.textContent = '🚀 GENERATE VIDEOS';
            }
        });
        
        function startPolling() {
            if (pollingInterval) clearInterval(pollingInterval);
            
            pollingInterval = setInterval(async () => {
                try {
                    const response = await fetch('/api/status');
                    const status = await response.json();
                    
                    // Update progress
                    const percent = status.total > 0 ? 
                        (status.progress / status.total) * 100 : 0;
                    progressFill.style.width = percent + '%';
                    progressFill.textContent = Math.round(percent) + '%';
                    
                    // Update status
                    if (status.running) {
                        statusText.textContent = `Generating ${status.progress}/${status.total}...`;
                    } else {
                        statusText.textContent = `Complete: ${status.progress}/${status.total}`;
                        generateBtn.disabled = false;
                        generateBtn.textContent = '🚀 GENERATE VIDEOS';
                        clearInterval(pollingInterval);
                    }
                    
                    // Update log
                    if (status.log && status.log.length > 0) {
                        log.innerHTML = status.log.slice(-20).map(entry => 
                            `<div class="log-entry ${entry.type || ''}">${entry.message}</div>`
                        ).join('');
                        log.scrollTop = log.scrollHeight;
                    }
                } catch (error) {
                    console.error('Polling error:', error);
                }
            }, 2000);
        }
    </script>
</body>
</html>
"""

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """Serve mobile-friendly interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    """Get generation status"""
    return jsonify(generation_status)

@app.route('/api/generate', methods=['POST'])
def generate():
    """Start video generation"""
    if generation_status['running']:
        return jsonify({'success': False, 'error': 'Generation already running'})
    
    data = request.json
    region = data.get('region', 'USA (National)')
    count = data.get('count', 5)
    engine = data.get('engine', 'stability')
    adult = data.get('adult', False)
    
    # Reset status
    generation_status['running'] = True
    generation_status['progress'] = 0
    generation_status['total'] = count
    generation_status['current_video'] = 0
    generation_status['log'] = []
    generation_status['results'] = []
    
    # Start generation in background
    thread = threading.Thread(
        target=run_generation,
        args=(region, count, engine, adult),
        daemon=True
    )
    thread.start()
    
    return jsonify({'success': True, 'message': 'Generation started'})

def run_generation(region, count, engine, adult):
    """Run generation process"""
    try:
        # Import studio functions
        sys.path.insert(0, str(BASE))
        
        # Use command-line interface instead of GUI
        cmd = [
            sys.executable,
            str(STUDIO_SCRIPT),
            '--region', region,
            '--count', str(count),
            '--engine', engine,
            '--headless'
        ]
        
        if adult:
            cmd.append('--adult')
        
        generation_status['log'].append({
            'message': f'Starting generation: {count} videos, region: {region}',
            'type': 'info'
        })
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(BASE)
        )
        
        # Read output
        for line in process.stdout:
            generation_status['log'].append({
                'message': line.strip(),
                'type': 'info'
            })
            
            # Update progress if we see "VIDEO X/Y"
            if 'VIDEO' in line and '/' in line:
                try:
                    parts = line.split('VIDEO')[1].split('/')
                    if len(parts) >= 2:
                        current = int(parts[0].strip().split()[0])
                        generation_status['progress'] = current
                        generation_status['current_video'] = current
                except:
                    pass
        
        process.wait()
        
        generation_status['running'] = False
        generation_status['progress'] = count
        
        generation_status['log'].append({
            'message': f'✅ Generation complete: {count} videos',
            'type': 'success'
        })
        
    except Exception as e:
        generation_status['running'] = False
        generation_status['log'].append({
            'message': f'❌ Error: {str(e)}',
            'type': 'error'
        })

@app.route('/api/videos')
def list_videos():
    """List generated videos"""
    youtube_dir = STUDIO_DIR / 'youtube_ready'
    if not youtube_dir.exists():
        return jsonify({'videos': []})
    
    videos = []
    for video_file in youtube_dir.glob('*.mp4'):
        videos.append({
            'name': video_file.name,
            'size': video_file.stat().st_size,
            'modified': datetime.fromtimestamp(video_file.stat().st_mtime).isoformat()
        })
    
    return jsonify({'videos': sorted(videos, key=lambda x: x['modified'], reverse=True)})

@app.route('/api/download/<filename>')
def download_video(filename):
    """Download video file"""
    video_path = STUDIO_DIR / 'youtube_ready' / filename
    if video_path.exists():
        return send_file(str(video_path), as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("="*70)
    print("ABRAHAM STUDIO - WEB SERVER")
    print("="*70)
    print(f"\n📱 Mobile Access:")
    print(f"   http://0.0.0.0:5000")
    print(f"\n💻 Local Access:")
    print(f"   http://localhost:5000")
    print(f"\n🌐 Network Access (from iPhone):")
    print(f"   http://[YOUR_IP]:5000")
    print(f"\n   Find your IP:")
    print(f"   Windows: ipconfig | findstr IPv4")
    print(f"   Or use: http://localhost:5000/ip")
    print("\n" + "="*70 + "\n")
    
    # Run on all interfaces (0.0.0.0) for mobile access
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

