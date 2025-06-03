from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from auth import SECRET_KEY
from game_state import game_state
import jwt

router = APIRouter()
clients = {}

@router.websocket("/ws/game")
async def game_ws(websocket: WebSocket, token: str = Query(...)):
    key = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        key = payload["discord_id"]

        await websocket.accept()
        print(f"✅ WebSocket accepté pour {payload['username']} ({key})")

        if key not in clients:
            clients[key] = []
        clients[key].append((websocket, payload))

        if not any(p["discord_id"] == key for p in game_state["players"]):
            game_state["players"].append(payload)

        await broadcast_players()

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        if key in clients:
            clients[key] = [c for c in clients[key] if c[0] != websocket]
            if not clients[key]:
                del clients[key]
        print(f"🔌 Déconnecté : {key}")
        await broadcast_players()

    except Exception as e:
        print("❌ Erreur WebSocket:", e)
        await websocket.close()

async def broadcast_players():
    all_players = [
        {
            "username": p["username"],
            "discord_id": p["discord_id"],
            "avatar": p["avatar"],
            "isAdmin": p["isAdmin"],
        }
        for p in game_state["players"]
    ]
    msg = {"type": "update_players", "players": all_players}
    for ws_list in clients.values():
        for ws, _ in ws_list:
            await ws.send_json(msg)
