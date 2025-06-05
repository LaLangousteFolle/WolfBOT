from fastapi import APIRouter
from game_roles import roles_catalog

router = APIRouter()

@router.get("/roles")
async def roles():
    return roles_catalog
