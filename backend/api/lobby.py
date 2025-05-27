# backend/api/lobby.py
from fastapi import APIRouter, Request
from backend.state import lobby, connections
from backend.models import JoinRequest
from fastapi.responses import JSONResponse
from backend.models import LobbyState
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


@router.get("/lobby", response_model=LobbyState)
def get_lobby():
    return LobbyState(players=lobby["players"], phase=lobby["phase"])


@router.post("/lobby/join")
async def join_lobby(req: JoinRequest):
    name = req.name

    if name and name not in lobby["players"]:
        lobby["players"].append(name)

        for ws in connections:
            await ws.send_text(
                json.dumps({"type": "join", "name": name, "players": lobby["players"]})
            )
        return {"message": f"{name} joined"}

    return {"error": "Nom invalide ou déjà pris"}
