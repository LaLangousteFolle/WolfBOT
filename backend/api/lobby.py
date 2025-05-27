# backend/api/lobby.py
from fastapi import APIRouter, Request
from backend.state import lobby, connections
from backend.models import JoinRequest, RoleConfigRequest
from fastapi.responses import JSONResponse
from backend.models import LobbyState
import json
import random

router = APIRouter()


@router.post("/lobby/start")
async def start_lobby():
    lobby["phase"] = "night"
    lobby["roles"] = {}

    roles_pool = generate_roles_from_config(lobby["role_config"])

    random.shuffle(lobby["players"])
    for player, role in zip(lobby["players"], roles_pool):
        lobby["roles"][player] = role

    # Broadcast aux clients (MAJ phase uniquement, on garde les rôles secrets)
    for ws in connections:
        await ws.send_text(
            json.dumps({"type": "start", "phase": "night", "players": lobby["players"]})
        )

    return {"message": "Partie lancée", "roles": lobby["roles"]}  # utile pour dev


@router.get("/lobby", response_model=LobbyState)
def get_lobby():
    return LobbyState(players=lobby["players"], phase=lobby["phase"])


@router.post("/lobby/config")
async def set_role_config(req: RoleConfigRequest):
    lobby["role_config"] = req.config
    return {"message": "Configuration mise à jour", "config": lobby["role_config"]}


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


def generate_roles_from_config(config: dict[str, int]) -> list[str]:
    roles = []
    for role, count in config.items():
        roles.extend([role] * count)
    return roles
