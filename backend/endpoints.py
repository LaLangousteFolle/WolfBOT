from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from websocket import router as ws_router
from game_logic import start_game, reset_game
from game_roles import roles_catalog
from auth import get_current_user
from fastapi import Depends, HTTPException
from game_state import game_state

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router)

@app.post("/start")
async def start_route(current_user: dict = Depends(get_current_user)):
    if not current_user["isAdmin"]:
        raise HTTPException(status_code=403)
    start_game()
    return {"detail": "Partie lancée"}

@app.get("/my-role")
async def my_role(current_user: dict = Depends(get_current_user)):
    for p in game_state["players"]:
        if p["discord_id"] == current_user["discord_id"]:
            return {"role": p.get("role", None)}
    raise HTTPException(status_code=404)

@app.get("/roles")
async def roles():
    return roles_catalog

