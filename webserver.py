import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from core.game_engine import GameEngine

# Chargement des variables d'environnement
load_dotenv()

# Initialisation de FastAPI
app = FastAPI()

# Ajoute le moteur de jeu
engine = GameEngine()

# CORS : autorise l'origine de ton front (Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # à adapter si tu déploies
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables d'environnement
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")  # Doit pointer vers /callback
FRONTEND_REDIRECT_URI = os.getenv("FRONTEND_REDIRECT_URI", "http://localhost:3000/dashboard")


@app.get("/login")
async def login():
    discord_auth_url = (
        "https://discord.com/api/oauth2/authorize"
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
        return HTMLResponse("<h1>Erreur: Pas de code OAuth2</h1>", status_code=400)

    # Échange du code contre un token
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify",
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    token_response = requests.post(
        "https://discord.com/api/oauth2/token", data=data, headers=headers
    )

    if token_response.status_code != 200:
        return HTMLResponse("<h1>Erreur: Token invalide</h1>", status_code=400)

    tokens = token_response.json()
    access_token = tokens["access_token"]

    # Récupération des infos utilisateur
    user_headers = {"Authorization": f"Bearer {access_token}"}
    user_resp = requests.get("https://discord.com/api/users/@me", headers=user_headers)

    if user_resp.status_code != 200:
        return HTMLResponse("<h1>Erreur: Impossible de récupérer les infos utilisateur</h1>", status_code=400)

    user_data = user_resp.json()
    user_id = user_data["id"]
    username = user_data["username"]
    avatar = user_data.get("avatar")

    avatar_url = (
    f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.png"
    if avatar else "https://cdn.discordapp.com/embed/avatars/0.png"
)

    # Ajout du joueur dans le moteur de jeu
    engine.add_player(user_id, username, avatar)

    # Rediriger avec avatar_url (URL-encodée si besoin)
    from urllib.parse import urlencode
    params = urlencode({
        "username": username,
        "id": user_id,
        "avatar": avatar_url
    })
    redirect_url = f"{FRONTEND_REDIRECT_URI}?{params}"
    return RedirectResponse(url=redirect_url)
