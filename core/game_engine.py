# core/game_engine.py

import random

ROLES = [
    "Loup-Garou",
    "Voyante",
    "Sorcière",
    "Villageois",
    "Cupidon",
    "Chasseur",
    "Corbeau",
    "Garde",
]


class Player:
    def __init__(self, id: str, username: str, avatar_url: str):
        self.id = id
        self.username = username
        self.avatar = avatar_url
        self.role = None
        self.alive = True

    def __repr__(self):
        return (
            f"<{self.username} - {self.role or '❓'} - {'🟢' if self.alive else '☠️'}>"
        )


class GameEngine:
    def __init__(self):
        self.players: dict[str, Player] = {}
        self.game_started = False
        self.phase = "lobby"

    def add_player(self, id: str, username: str, avatar_url: str) -> bool:
        if self.game_started or id in self.players:
            return False
        self.players[id] = Player(id, username, avatar_url)
        return True

    def get_state(self):
        return {
            "started": self.game_started,
            "phase": self.phase,
            "players": [
                {"id": p.id, "name": p.username, "avatar": p.avatar, "alive": p.alive}
                for p in self.players.values()
            ],
        }
