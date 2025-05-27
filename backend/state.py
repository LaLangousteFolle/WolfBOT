# backend/state.py
lobby = {
    "players": [],
    "phase": "waiting",
    "roles": {},
    "role_config": {
        "loup": 2,
        "voyante": 1,
        "villageois": 3
    }
}

connections = set()
