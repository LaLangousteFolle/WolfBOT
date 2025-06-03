from game_state import game_state
import random

AVAILABLE_ROLES = ["Loup", "Voyante", "Villageois", "Villageois", "Villageois"]

def start_game():
    players = game_state["players"]
    num_players = len(players)
    if num_players < 3:
        raise Exception("Pas assez de joueurs")
    
    roles = AVAILABLE_ROLES[:num_players]
    random.shuffle(roles)

    for i, p in enumerate(players):
        p["role"] = roles[i]

    game_state["phase"] = "roles_assigned"

def reset_game():
    game_state["players"] = []
    game_state["phase"] = "waiting"
