# backend/api/lobby.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from backend.state import lobby, connections
import json

router = APIRouter()


@router.post("/lobby/start")
async def start_lobby():
    lobby["players"] = []
    lobby["phase"] = "waiting"

    # Notifie tous les clients WebSocket
    for ws in connections:
        await ws.send_text(
            json.dumps({"type": "start", "phase": "waiting", "players": []})
        )

    return {"message": "Lobby started"}


@router.post("/lobby/join")
async def join_lobby(request: Request):
    data = await request.json()
    name = data.get("name")

    if name and name not in lobby["players"]:
        lobby["players"].append(name)

        # Notifie tous les clients WebSocket
        for ws in connections:
            await ws.send_text(
                json.dumps({"type": "join", "name": name, "players": lobby["players"]})
            )
        return {"message": f"{name} joined"}
    return JSONResponse(status_code=400, content={"error": "Nom invalide ou déjà pris"})
