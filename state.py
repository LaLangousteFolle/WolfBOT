# state.py

# Game state variable
game_active = False
players = {}
votes = {}
wolf_votes = {}
dead_players = set()
current_phase = None

# Special roles
voyante = None
sorciere = None
cupidon = None
chasseur = None
amoureux_pair = []  # Two lovers there
corbeau = None
corbeau_target = None

# Special channels
log_channel = None
wolf_channel = None
seer_channel = None
witch_channel = None
voice_channel = None
cupidon_channel = None
amoureux_channel = None

# Action's gestion
witch_heal_used = False
witch_kill_used = False
vision_used = False
victim_of_wolves = None
victim_of_witch = None

# Gestion join
join_locked = False
join_message = None
join_users = []

# Locks
vote_lock = None
tir_cible = None  # Cible du Chasseur après sa mort
