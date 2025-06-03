from pydantic import BaseModel

class Player(BaseModel):
    username: str
    discord_id: str
    avatar: str
    isAdmin: bool
