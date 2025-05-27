# backend/models.py

from pydantic import BaseModel
from typing import List


class JoinRequest(BaseModel):
    name: str


class LobbyState(BaseModel):
    players: List[str]
    phase: str
