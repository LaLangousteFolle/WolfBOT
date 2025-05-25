import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from dotenv import load_dotenv
from core.game_engine import GameEngine

engine = GameEngine()
load_dotenv()

app = FastAPI()

CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")


@app.get("/login")
async def login():
    discord_auth_url = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify"
    )
    return RedirectResponse(discord_auth_url)


@app.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return HTMLResponse("<h1>Erreur: Pas de code OAuth2</h1>")

    # Échange code contre token
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify",
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    r = requests.post(
        "https://discord.com/api/oauth2/token", data=data, headers=headers
    )
    r.raise_for_status()
    tokens = r.json()
    access_token = tokens["access_token"]

    # Récup info utilisateur
    headers = {"Authorization": f"Bearer {access_token}"}
    user_resp = requests.get("https://discord.com/api/users/@me", headers=headers)
    user_data = user_resp.json()

    # ➕ Ici tu ajoutes le joueur dans ton moteur de jeu
    user_id = user_data["id"]
    username = user_data["username"]
    avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{user_data['avatar']}.png"

    # → Tu peux maintenant appeler game_engine.add_player(...)
    return HTMLResponse(
        f"<h1>Bienvenue {username}!</h1><img src='{avatar}' width='128' />"
    )
