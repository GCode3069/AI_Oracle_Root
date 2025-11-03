"""
DISTRIBUTED VIDEO GENERATION SYSTEM
Use multiple machines to speed up video production
"""
import os, json, socket, time, subprocess
from pathlib import Path
from datetime import datetime
import http.server
import socketserver
import threading

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
PORT = 8888

class VideoTask:
    def __init__(self, task_id, generator, count, priority=0):
        self.task_id = task_id
        self.generator = generator
        self.count = count
        self.priority = priority
        self.status = "pending"
        self.assigned_to = None
        self.created = datetime.now().isoformat()
        self.started = None
        self.completed = None
        self.videos_generated = []

class DistributedVideoServer:
    """Master server that distributes video generation tasks"""
    
    def __init__(self, port=PORT):
        self.port = port
        self.tasks = []
        self.workers = {}
        self.task_id_counter = 0
    
    def add_task(self, generator, count, priority=0):
        """Add a new video generation task"""
        task = VideoTask(self.task_id_counter, generator, count, priority)
        self.tasks.append(task)
        self.task_id_counter += 1
        print(f"[OK] Task {task.task_id} added: {generator} x{count}")
        return task.task_id
    
    def get_next_task(self, worker_id):
        """Get next available task for a worker"""
        # Find highest priority pending task
        pending = [t for t in self.tasks if t.status == "pending"]
        if not pending:
            return None
        
        task = max(pending, key=lambda t: t.priority)
        task.status = "running"
        task.assigned_to = worker_id
        task.started = datetime.now().isoformat()
        
        print(f"[PROCESS] Task {task.task_id} assigned to {worker_id}")
        return task
    
    def complete_task(self, task_id, videos):
        """Mark task as complete"""
        task = next((t for t in self.tasks if t.task_id == task_id), None)
        if task:
            task.status = "completed"
            task.completed = datetime.now().isoformat()
            task.videos_generated = videos
            print(f"[OK] Task {task_id} completed: {len(videos)} videos")
    
    def get_status(self):
        """Get system status"""
        return {
            'workers': len(self.workers),
            'pending': len([t for t in self.tasks if t.status == "pending"]),
            'running': len([t for t in self.tasks if t.status == "running"]),
            'completed': len([t for t in self.tasks if t.status == "completed"]),
            'tasks': [
                {
                    'id': t.task_id,
                    'generator': t.generator,
                    'count': t.count,
                    'status': t.status,
                    'worker': t.assigned_to
                }
                for t in self.tasks
            ]
        }

class VideoWorker:
    """Worker that runs on any machine to process video tasks"""
    
    def __init__(self, server_ip, port=PORT, name=None):
        self.server_ip = server_ip
        self.port = port
        self.name = name or socket.gethostname()
        self.running = False
    
    def connect(self):
        """Connect to master server"""
        print(f"[PROCESS] Worker '{self.name}' connecting to {self.server_ip}:{self.port}...")
        # In real implementation, this would use actual network connection
        print(f"[OK] Worker '{self.name}' connected")
    
    def run(self):
        """Main worker loop"""
        self.running = True
        print(f"[OK] Worker '{self.name}' started")
        
        while self.running:
            # Request task from server
            task = self.request_task()
            
            if task:
                # Execute task
                print(f"[PROCESS] Worker '{self.name}' executing: {task['generator']} x{task['count']}")
                videos = self.execute_task(task)
                
                # Report completion
                self.report_completion(task['id'], videos)
            else:
                # No tasks available, wait
                print(f"[INFO] Worker '{self.name}' idle, waiting 30s...")
                time.sleep(30)
    
    def request_task(self):
        """Request next task from server"""
        # Placeholder - in real implementation, this would be HTTP/socket request
        return None
    
    def execute_task(self, task):
        """Execute a video generation task"""
        try:
            generator = task['generator']
            count = task['count']
            
            # Run the generator
            cmd = f"cd {BASE} && python -Xutf8 {generator} {count}"
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            
            # Return generated video paths
            uploaded = BASE / "uploaded"
            videos = sorted(uploaded.glob("*.mp4"), key=lambda x: x.stat().st_mtime)[-count:]
            return [str(v) for v in videos]
        
        except Exception as e:
            print(f"[ERROR] Task execution failed: {e}")
            return []
    
    def report_completion(self, task_id, videos):
        """Report task completion to server"""
        print(f"[OK] Worker '{self.name}' completed task {task_id}: {len(videos)} videos")

# Simple file-based coordination (for initial setup)
class FileBasedCoordinator:
    """Simple file-based task coordination (works without network setup)"""
    
    def __init__(self, base_path=BASE):
        self.base = Path(base_path)
        self.queue_dir = self.base / "queue"
        self.queue_dir.mkdir(exist_ok=True)
        self.running_dir = self.base / "running"
        self.running_dir.mkdir(exist_ok=True)
        self.completed_dir = self.base / "completed"
        self.completed_dir.mkdir(exist_ok=True)
    
    def add_task(self, generator, count, priority=0):
        """Add task to queue"""
        task_id = int(time.time() * 1000)
        task = {
            'id': task_id,
            'generator': generator,
            'count': count,
            'priority': priority,
            'created': datetime.now().isoformat()
        }
        
        task_file = self.queue_dir / f"{priority:03d}_{task_id}.json"
        with open(task_file, 'w') as f:
            json.dump(task, f, indent=2)
        
        print(f"[OK] Task {task_id} queued: {generator} x{count}")
        return task_id
    
    def get_next_task(self, worker_id="unknown"):
        """Get next task from queue"""
        tasks = sorted(self.queue_dir.glob("*.json"))
        if not tasks:
            return None
        
        # Get highest priority task
        task_file = tasks[0]
        with open(task_file, 'r') as f:
            task = json.load(f)
        
        # Move to running
        running_file = self.running_dir / f"{task['id']}_{worker_id}.json"
        task['worker'] = worker_id
        task['started'] = datetime.now().isoformat()
        
        with open(running_file, 'w') as f:
            json.dump(task, f, indent=2)
        
        task_file.unlink()
        print(f"[PROCESS] Task {task['id']} assigned to {worker_id}")
        return task
    
    def complete_task(self, task_id, worker_id="unknown", videos=None):
        """Mark task as completed"""
        running_file = self.running_dir / f"{task_id}_{worker_id}.json"
        if running_file.exists():
            with open(running_file, 'r') as f:
                task = json.load(f)
            
            task['completed'] = datetime.now().isoformat()
            task['videos'] = videos or []
            
            completed_file = self.completed_dir / f"{task_id}.json"
            with open(completed_file, 'w') as f:
                json.dump(task, f, indent=2)
            
            running_file.unlink()
            print(f"[OK] Task {task_id} completed")
    
    def get_status(self):
        """Get system status"""
        queued = len(list(self.queue_dir.glob("*.json")))
        running = len(list(self.running_dir.glob("*.json")))
        completed = len(list(self.completed_dir.glob("*.json")))
        
        return {
            'queued': queued,
            'running': running,
            'completed': completed
        }

def setup_worker_script():
    """Create worker script for older laptop"""
    worker_script = BASE / "WORKER_START.py"
    
    with open(worker_script, 'w') as f:
        f.write('''"""
WORKER NODE - Run on older laptop
Processes video generation tasks
"""
import sys, time, socket, subprocess
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from DISTRIBUTED_VIDEO_SYSTEM import FileBasedCoordinator

BASE = Path(__file__).parent
WORKER_ID = socket.gethostname()

print(f"{'='*70}")
print(f"VIDEO WORKER: {WORKER_ID}")
print(f"{'='*70}\\n")

coordinator = FileBasedCoordinator(BASE)

while True:
    # Check status
    status = coordinator.get_status()
    print(f"[STATUS] Queue: {status['queued']}, Running: {status['running']}, Done: {status['completed']}")
    
    # Get next task
    task = coordinator.get_next_task(WORKER_ID)
    
    if task:
        print(f"\\n[PROCESS] Executing: {task['generator']} x{task['count']}")
        print(f"{'='*70}\\n")
        
        try:
            # Run generator
            cmd = f"cd {BASE} && python -Xutf8 {task['generator']} {task['count']}"
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(result.stdout)
            
            # Find generated videos
            uploaded = BASE / "uploaded"
            videos = sorted(uploaded.glob("*.mp4"), key=lambda x: x.stat().st_mtime)[-task['count']:]
            video_paths = [str(v) for v in videos]
            
            # Mark complete
            coordinator.complete_task(task['id'], WORKER_ID, video_paths)
            
            print(f"\\n[OK] Task {task['id']} completed: {len(video_paths)} videos")
        
        except Exception as e:
            print(f"[ERROR] Task failed: {e}")
            coordinator.complete_task(task['id'], WORKER_ID, [])
    
    else:
        print("[INFO] No tasks available, waiting 60s...\\n")
        time.sleep(60)
''')
    
    print(f"[OK] Worker script created: {worker_script.name}")
    return worker_script

if __name__ == "__main__":
    print(f"\n{'='*70}")
    print(f"DISTRIBUTED VIDEO GENERATION SYSTEM")
    print(f"{'='*70}\n")
    
    # Create coordinator
    coordinator = FileBasedCoordinator(BASE)
    
    # Create worker script
    worker_script = setup_worker_script()
    
    print(f"\n{'='*70}")
    print(f"SETUP COMPLETE")
    print(f"{'='*70}\n")
    
    print("TO USE THIS SYSTEM:")
    print("\n1. ON MAIN MACHINE:")
    print("   - Queue tasks using:")
    print("     from DISTRIBUTED_VIDEO_SYSTEM import FileBasedCoordinator")
    print("     coordinator = FileBasedCoordinator()")
    print("     coordinator.add_task('ULTIMATE_HORROR_GENERATOR.py', 10, priority=5)")
    print("\n2. ON OLDER LAPTOP:")
    print(f"   - Copy entire folder: {BASE}")
    print("   - Install Python & dependencies")
    print("   - Run: python WORKER_START.py")
    print("\n3. BOTH MACHINES:")
    print("   - Use shared folder (network drive, Dropbox, etc.)")
    print("   - Or sync queue/running/completed folders manually")
    
    print("\n\n{'='*70}")
    print("EXAMPLE: Queue 50 videos across 5 generators")
    print("{'='*70}\n")
    
    # Example: Queue tasks
    coordinator.add_task("ULTIMATE_HORROR_GENERATOR.py", 10, priority=10)
    coordinator.add_task("PROJECT_COGNITOHAZARD.py", 5, priority=9)
    coordinator.add_task("DARK_JOSH_DYNAMIC.py", 15, priority=8)
    coordinator.add_task("MULTI_PLATFORM_ENGINE.py", 10, priority=7)
    coordinator.add_task("QR_CODE_VIRAL_GENERATOR.py", 10, priority=6)
    
    status = coordinator.get_status()
    print(f"\n[OK] {status['queued']} tasks queued")
    print("\nStart workers on both machines to process tasks!")

