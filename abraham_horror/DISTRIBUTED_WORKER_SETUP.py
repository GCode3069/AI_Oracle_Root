"""
DISTRIBUTED WORKER SETUP
Sets up older laptop to help with video generation workload
Uses shared network folder for task distribution
"""
import os, sys, json, time, socket
from pathlib import Path
from datetime import datetime

# Configuration
MAIN_PC = "F:/AI_Oracle_Root/scarify/abraham_horror"
NETWORK_SHARE = "\\\\MAIN_PC\\scarify_tasks"  # Update with your actual network path
WORKER_ID = socket.gethostname()

class DistributedWorker:
    """Worker node for distributed video generation"""
    
    def __init__(self, worker_id=None):
        self.worker_id = worker_id or WORKER_ID
        self.tasks_dir = Path(NETWORK_SHARE) if Path(NETWORK_SHARE).exists() else Path(MAIN_PC)
        self.queue_dir = self.tasks_dir / "queue"
        self.processing_dir = self.tasks_dir / "processing"
        self.completed_dir = self.tasks_dir / "completed"
        self.failed_dir = self.tasks_dir / "failed"
        
        self.setup_directories()
    
    def setup_directories(self):
        """Create work directories"""
        print(f"[WORKER] Setting up directories for {self.worker_id}...")
        
        for dir_path in [self.queue_dir, self.processing_dir, self.completed_dir, self.failed_dir]:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"[SETUP] ✓ {dir_path}")
            except Exception as e:
                print(f"[SETUP] ✗ {dir_path}: {e}")
    
    def create_task(self, task_type, params):
        """Create a new task (called from main PC)"""
        task_id = f"{task_type}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        task_file = self.queue_dir / f"{task_id}.json"
        
        task_data = {
            'task_id': task_id,
            'task_type': task_type,
            'params': params,
            'created': datetime.now().isoformat(),
            'status': 'queued',
            'worker': None
        }
        
        with open(task_file, 'w') as f:
            json.dump(task_data, f, indent=2)
        
        print(f"[TASK] Created: {task_id}")
        return task_id
    
    def get_next_task(self):
        """Get next available task from queue"""
        tasks = list(self.queue_dir.glob("*.json"))
        
        if not tasks:
            return None
        
        # Get oldest task
        task_file = sorted(tasks, key=lambda x: x.stat().st_ctime)[0]
        
        try:
            with open(task_file, 'r') as f:
                task = json.load(f)
            
            # Move to processing
            processing_file = self.processing_dir / task_file.name
            task_file.rename(processing_file)
            
            # Update task
            task['status'] = 'processing'
            task['worker'] = self.worker_id
            task['started'] = datetime.now().isoformat()
            
            with open(processing_file, 'w') as f:
                json.dump(task, f, indent=2)
            
            print(f"[WORKER] Claimed task: {task['task_id']}")
            return task, processing_file
            
        except Exception as e:
            print(f"[ERROR] Failed to claim task: {e}")
            return None
    
    def execute_task(self, task, task_file):
        """Execute a task based on type"""
        print(f"\n[EXEC] Starting: {task['task_type']}")
        
        task_type = task['task_type']
        params = task['params']
        
        try:
            if task_type == 'generate_video':
                result = self.generate_video(**params)
            elif task_type == 'add_qr_code':
                result = self.add_qr_code(**params)
            elif task_type == 'process_audio':
                result = self.process_audio(**params)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
            
            # Mark complete
            task['status'] = 'completed'
            task['completed'] = datetime.now().isoformat()
            task['result'] = result
            
            completed_file = self.completed_dir / task_file.name
            with open(completed_file, 'w') as f:
                json.dump(task, f, indent=2)
            
            task_file.unlink()  # Remove from processing
            
            print(f"[EXEC] ✓ Completed: {task['task_id']}")
            return True
            
        except Exception as e:
            print(f"[EXEC] ✗ Failed: {e}")
            
            # Mark failed
            task['status'] = 'failed'
            task['failed'] = datetime.now().isoformat()
            task['error'] = str(e)
            
            failed_file = self.failed_dir / task_file.name
            with open(failed_file, 'w') as f:
                json.dump(task, f, indent=2)
            
            task_file.unlink()
            return False
    
    def generate_video(self, generator_type, script, headline):
        """Generate video using specified generator"""
        print(f"[VIDEO] Generating with {generator_type}...")
        
        # Import appropriate generator
        if generator_type == 'ultimate_horror':
            from ULTIMATE_HORROR_GENERATOR import generate_horror_video
            return generate_horror_video(script, headline)
        elif generator_type == 'cognitohazard':
            from PROJECT_COGNITOHAZARD import generate_cognitohazard_episode
            return generate_cognitohazard_episode()
        else:
            raise ValueError(f"Unknown generator: {generator_type}")
    
    def add_qr_code(self, video_path, qr_path):
        """Add QR code to video"""
        print(f"[QR] Adding to {video_path}...")
        from FIX_QR_CODES_BATCH import add_qr_to_video
        return add_qr_to_video(video_path, qr_path)
    
    def process_audio(self, script, voice_id):
        """Generate audio"""
        print(f"[AUDIO] Generating with voice {voice_id}...")
        # Import from existing generators
        return {"audio_path": "temp/audio.mp3"}
    
    def run_worker(self, check_interval=10):
        """Run worker loop"""
        print("\n" + "="*70)
        print(f"DISTRIBUTED WORKER: {self.worker_id}")
        print("="*70)
        print(f"[WORKER] Watching: {self.queue_dir}")
        print(f"[WORKER] Check interval: {check_interval}s")
        print("[WORKER] Press Ctrl+C to stop")
        print("="*70 + "\n")
        
        tasks_completed = 0
        
        try:
            while True:
                result = self.get_next_task()
                
                if result:
                    task, task_file = result
                    success = self.execute_task(task, task_file)
                    if success:
                        tasks_completed += 1
                        print(f"[STATS] Total completed: {tasks_completed}")
                else:
                    print(f"[WORKER] No tasks. Waiting {check_interval}s...")
                    time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print(f"\n[WORKER] Stopped. Completed {tasks_completed} tasks.")

# Task Creation Functions (for main PC)

def distribute_video_generation(scripts, generator_type='ultimate_horror'):
    """Distribute video generation across workers"""
    worker = DistributedWorker()
    
    print(f"\n[DISTRIBUTE] Creating {len(scripts)} video generation tasks...")
    
    task_ids = []
    for i, script_data in enumerate(scripts):
        task_id = worker.create_task('generate_video', {
            'generator_type': generator_type,
            'script': script_data.get('script'),
            'headline': script_data.get('headline')
        })
        task_ids.append(task_id)
        print(f"  [{i+1}/{len(scripts)}] Queued: {task_id}")
    
    print(f"\n[DISTRIBUTE] ✓ Created {len(task_ids)} tasks")
    print(f"[DISTRIBUTE] Workers can now process from: {worker.queue_dir}")
    
    return task_ids

def distribute_qr_fixes(video_files, qr_image_path):
    """Distribute QR code addition across workers"""
    worker = DistributedWorker()
    
    print(f"\n[DISTRIBUTE] Creating {len(video_files)} QR fix tasks...")
    
    task_ids = []
    for video_path in video_files:
        task_id = worker.create_task('add_qr_code', {
            'video_path': str(video_path),
            'qr_path': str(qr_image_path)
        })
        task_ids.append(task_id)
    
    print(f"\n[DISTRIBUTE] ✓ Created {len(task_ids)} QR fix tasks")
    return task_ids

def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Distributed Video Generation Worker')
    parser.add_argument('--mode', choices=['worker', 'distribute'], default='worker',
                       help='Run as worker or distribute tasks')
    parser.add_argument('--count', type=int, default=10,
                       help='Number of tasks to create (distribute mode)')
    
    args = parser.parse_args()
    
    if args.mode == 'worker':
        worker = DistributedWorker()
        worker.run_worker()
    else:
        # Example: Create 10 video generation tasks
        scripts = [{'script': f'Test script {i}', 'headline': f'Headline {i}'} for i in range(args.count)]
        distribute_video_generation(scripts)

if __name__ == "__main__":
    main()

