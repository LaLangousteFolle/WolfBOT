# backend/state.py
lobby = {
    "players": [],
    "phase": "waiting",
    "roles": {},  # final assignments
    "role_config": {},  # ex: { "loup": 2, "voyante": 1, "villageois": 3 }
}
connections = set()
