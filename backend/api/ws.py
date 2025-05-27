# backend/api/ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.state import connections, lobby
import json

router = APIRouter()


@router.websocket("/ws/lobby")
async def websocket_lobby(websocket: WebSocket):
    await websocket.accept()
    connections.add(websocket)

    # Envoie l’état initial
    await websocket.send_text(
        json.dumps(
            {"type": "init", "phase": lobby["phase"], "players": lobby["players"]}
        )
    )

    try:
        while True:
            await websocket.receive_text()  # ignore les messages reçus pour l'instant
    except WebSocketDisconnect:
        connections.remove(websocket)
