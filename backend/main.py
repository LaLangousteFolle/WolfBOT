from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
import jwt

SECRET_KEY = "votre_clé_ultra_secrète"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En prod : restreindre à ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dictionnaire des connexions par joueur
clients = {}

def generate_token(discord_id, username, avatar_url):
    payload = {
        "discord_id": discord_id,
        "username": username,
        "avatar": avatar_url,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


@app.websocket("/ws/game")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    key = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        key = payload["discord_id"]

        await websocket.accept()
        print(f"✅ WebSocket accepté pour {payload['username']} ({key})")

        if key not in clients:
            clients[key] = []

        clients[key].append((websocket, payload))
        await broadcast_players()

        while True:
            data = await websocket.receive_text()
            print("📩 Message reçu :", data)

    except WebSocketDisconnect:
        print(f"🔌 Déconnexion WebSocket pour {key}")
        if key in clients:
            clients[key] = [
                (ws, p) for ws, p in clients[key] if ws != websocket
            ]
            if not clients[key]:
                del clients[key]
            await broadcast_players()

    except jwt.ExpiredSignatureError:
        await websocket.close(code=4001)
        print("❌ Token expiré")
    except Exception as e:
        print("❌ Erreur WebSocket:", e)
        await websocket.close(code=4002)


async def broadcast_players():
    all_players = [
        {
            "username": p["username"],
            "discord_id": p["discord_id"],
            "avatar": p["avatar"]
        }
        for ws_list in clients.values()
        for _, p in ws_list
    ]
    message = {"type": "update_players", "players": all_players}

    for ws_list in clients.values():
        for ws, _ in ws_list:
            await ws.send_json(message)
