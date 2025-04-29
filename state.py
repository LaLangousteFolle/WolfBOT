# state.py

game_active = False
players = {}
votes = {}
wolf_votes = {}
dead_players = set()
current_phase = None
join_locked = False
join_message = None
join_users = []
vote_lock = None

# Salons
log_channel = None
wolf_channel = None
seer_channel = None
witch_channel = None
voice_channel = None

# Rôles spéciaux
voyante = None
sorciere = None
witch_heal_used = False
witch_kill_used = False
vision_used = False
victim_of_wolves = None
victim_of_witch = None
guild = None
