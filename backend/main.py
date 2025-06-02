from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import jwt
import datetime

SECRET_KEY = "votre_clé_ultra_secrète"

app = FastAPI()

# Autoriser le CORS pour ton frontend (localhost:3000 par exemple)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clients connectés : { game_id: [WebSocket, ...] }
clients = {}

# Générateur de lien/token
def generate_token(discord_id, username, avatar_url, game_id):
    payload = {
        "discord_id": discord_id,
        "username": username,
        "avatar": avatar_url,
        "game_id": game_id,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


@app.websocket("/ws/game/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, token: str = Query(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        await websocket.accept()

        if game_id not in clients:
            clients[game_id] = []

        clients[game_id].append((websocket, payload))

        # Broadcast de la liste des joueurs
        await broadcast_players(game_id)

        while True:
            data = await websocket.receive_text()
            print("Message reçu :", data)
            # Traite les messages si nécessaire

    except WebSocketDisconnect:
        if game_id in clients:
            clients[game_id] = [
                (ws, p) for ws, p in clients[game_id] if ws != websocket
            ]
            await broadcast_players(game_id)

    except jwt.ExpiredSignatureError:
        await websocket.close(code=4001)
    except Exception as e:
        print("Erreur WebSocket:", e)


async def broadcast_players(game_id: str):
    players = [
        {
            "username": p["username"],
            "discord_id": p["discord_id"],
            "avatar": p["avatar"]
        }
        for _, p in clients.get(game_id, [])
    ]
    message = {"type": "update_players", "players": players}

    for ws, _ in clients.get(game_id, []):
        await ws.send_json(message)
