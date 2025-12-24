from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from .orchestrator.deb8 import DebateManager

app = FastAPI()
manager = DebateManager()

@app.get("/health")
async def health():
    return {"status": "vertex_active", "mode": "hybrid"}

@app.websocket("/ws/debate")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.process_message(websocket, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)