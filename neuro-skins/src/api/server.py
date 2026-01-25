"""
NeuroSkins API Server
REST API and WebSocket for system control
"""

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import asyncio
import json

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.system import create_system
from src.core.config import ProductTier


# API Models
class SessionStartRequest(BaseModel):
    tier: str = "lite"
    user_id: str = "default"
    age: int = 25
    duration_minutes: int = 20


class SessionResponse(BaseModel):
    session_id: str
    status: str
    message: str


class StatusResponse(BaseModel):
    tier: str
    running: bool
    session_active: bool
    safety_score: float
    current_protocol: Optional[str]


# Global system instance
neuroskins_system = None


# Create FastAPI app
app = FastAPI(
    title="NeuroSkins API",
    description="Adaptive Neural Interface API",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "NeuroSkins × Frequency Fusion",
        "version": "0.1.0",
        "status": "operational"
    }


@app.get("/tiers")
async def get_tiers():
    """Get available product tiers"""
    return {
        "tiers": [
            {
                "name": "lite",
                "price": 299,
                "features": ["Basic 40 Hz gamma", "Trauma deletion"]
            },
            {
                "name": "pro",
                "price": 899,
                "features": ["Full protocol suite", "HRV monitoring", "Cortisol tracking"]
            },
            {
                "name": "ascend",
                "price": 2499,
                "features": ["Sex synchronization", "Ego death protocol", "Float tank"]
            }
        ]
    }


@app.get("/protocols")
async def get_protocols(tier: str = "lite"):
    """Get available protocols for tier"""
    from src.protocols.library import get_protocols_for_tier
    
    protocols = get_protocols_for_tier(tier)
    
    return {
        "tier": tier,
        "protocols": [
            {
                "name": protocol.name,
                "type": protocol.protocol_type.value,
                "description": protocol.description,
                "duration": protocol.expected_duration,
                "age_restriction": protocol.age_restriction
            }
            for protocol in protocols
        ]
    }


@app.post("/session/start", response_model=SessionResponse)
async def start_session(request: SessionStartRequest):
    """Start a new NeuroSkins session"""
    global neuroskins_system
    
    try:
        # Create system if not exists
        if neuroskins_system is None or neuroskins_system.config.tier.value != request.tier:
            neuroskins_system = create_system(
                tier=request.tier,
                user_id=request.user_id
            )
        
        # Verify age
        if not neuroskins_system.verify_user_age(request.age):
            raise HTTPException(status_code=403, detail="Age verification failed")
        
        # Initialize hardware
        if not neuroskins_system.initialize_hardware():
            raise HTTPException(status_code=500, detail="Hardware initialization failed")
        
        # Start session
        session_id = neuroskins_system.start_session()
        
        # Run in background
        asyncio.create_task(
            run_session_async(neuroskins_system, request.duration_minutes)
        )
        
        return SessionResponse(
            session_id=session_id,
            status="started",
            message=f"Session started for {request.duration_minutes} minutes"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def run_session_async(system, duration_minutes: int):
    """Run session asynchronously"""
    try:
        # Run closed-loop in thread to avoid blocking
        import threading
        thread = threading.Thread(
            target=system.run_closed_loop,
            args=(duration_minutes,)
        )
        thread.start()
    except Exception as e:
        print(f"[ERROR] Session error: {e}")


@app.post("/session/stop")
async def stop_session():
    """Stop current session"""
    global neuroskins_system
    
    if neuroskins_system is None:
        raise HTTPException(status_code=404, detail="No active system")
    
    neuroskins_system.stop_session()
    
    return {"status": "stopped", "message": "Session stopped"}


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get system status"""
    global neuroskins_system
    
    if neuroskins_system is None:
        raise HTTPException(status_code=404, detail="No active system")
    
    status = neuroskins_system.get_status()
    
    return StatusResponse(
        tier=status['tier'],
        running=status['running'],
        session_active=status['session']['active'] if status['session'] else False,
        safety_score=status['safety']['safety_score'],
        current_protocol=status['delivery'].get('current_protocol')
    )


@app.get("/status/detailed")
async def get_detailed_status():
    """Get detailed system status"""
    global neuroskins_system
    
    if neuroskins_system is None:
        raise HTTPException(status_code=404, detail="No active system")
    
    return neuroskins_system.get_status()


@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await websocket.accept()
    
    global neuroskins_system
    
    try:
        while True:
            if neuroskins_system and neuroskins_system.running:
                # Stream status updates
                status = neuroskins_system.get_status()
                await websocket.send_text(json.dumps(status))
            
            await asyncio.sleep(1)  # Update every second
            
    except Exception as e:
        print(f"[ERROR] WebSocket error: {e}")
    finally:
        await websocket.close()


def main():
    """Run API server"""
    import uvicorn
    
    print("=" * 60)
    print("NeuroSkins API Server")
    print("=" * 60)
    print("Starting server on http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
