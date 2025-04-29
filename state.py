# state.py

# Variables d'état du jeu
game_active = False
players = {}
votes = {}
wolf_votes = {}
dead_players = set()
current_phase = None

# Rôles spéciaux
voyante = None
sorciere = None
cupidon = None
chasseur = None
amoureux_pair = []  # Deux amoureux ici

# Channel spéciaux
log_channel = None
wolf_channel = None
seer_channel = None
witch_channel = None
voice_channel = None
cupidon_channel = None
amoureux_channel = None

# Gestion actions
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
