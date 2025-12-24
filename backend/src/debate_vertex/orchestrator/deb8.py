import time
import uuid
from fastapi import WebSocket
from ..models.brain_router import HybridBrain
from .cue_extractors import estimate_debate_pressure
from .state import DebateState

class DebateManager:
    def __init__(self):
        self.active_connections = {}
        self.brain = HybridBrain()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        session_id = str(uuid.uuid4())
        self.active_connections[websocket] = DebateState(session_id=session_id)
        print(f"Session {session_id} connected.")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            del self.active_connections[websocket]

    async def process_message(self, websocket: WebSocket, data: dict):
        state = self.active_connections[websocket]
        user_text = data.get("text", "")
        timer_remaining = data.get("timer", 30.0)
        
        # 1. Update State
        state.last_rebuttal_timer = timer_remaining
        state.add_turn("user", user_text)
        
        # 2. Analyze Pressure (The Nervous System)
        pressure = estimate_debate_pressure(user_text, timer_remaining)
        state.pressure_score = pressure
        
        # 3. Stream Thinking Status
        await websocket.send_json({
            "type": "status", 
            "pressure": pressure,
            "tier": "APEX_CLOUD" if pressure > 7.2 else "LOCAL_WARM"
        })
        
        # 4. Generate Response (The Brain)
        response_text = await self.brain.generate(state, state.get_context())
        state.add_turn("assistant", response_text)
        
        # 5. Send Response
        await websocket.send_json({
            "type": "response", 
            "text": response_text
        })