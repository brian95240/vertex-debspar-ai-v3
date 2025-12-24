from pydantic import BaseModel
from typing import List, Optional
import time

class DebateState(BaseModel):
    session_id: str
    history: List[dict] = []
    last_rebuttal_timer: float = 0.0
    pressure_score: float = 0.0
    turn_count: int = 0
    
    def add_turn(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        self.turn_count += 1
        
    def get_context(self, limit: int = 10) -> List[dict]:
        return self.history[-limit:]