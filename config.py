# config.py

# Channel IDs
log_channel_id = 1366109644707070032  # put your log channel id
wolf_channel_id = 1365955043215278111  # put your wolf channel id
seer_channel_id = 1366063228240789584  # put your seer channel id
witch_channel_id = 1366063263996973077  # put your witch channel id
voice_channel_id = 1366017756171866203  # put your voice channel id
cupidon_channel_id = 1366699130071547955  # put your cupidon channel id
amoureux_channel_id = 1366699189941305354  # put your lovers channel id
corbeau_channel_id = 1375427738739019776  # put your crow channel id
garde_channel_id = 1375447606330916925  # put your gard channel id

# Roles config
ROLES_CONFIG = {
    "Loup-Garou": {"quantity": 0, "team": "mal", "emoji": "🐺"},
    "Voyante": {"quantity": 0, "team": "bon", "emoji": "🔮"},
    "Villageois": {"quantity": 0, "team": "bon", "emoji": "👨‍🌾"},
    "Sorcière": {"quantity": 0, "team": "bon", "emoji": "🧙‍♀️"},
    "Cupidon": {"quantity": 0, "team": "bon", "emoji": "💘"},
    "Chasseur": {"quantity": 0, "team": "bon", "emoji": "🏹"},
    "Corbeau": {"quantity": 0, "team": "bon", "emoji": "🪶"},
    "Garde": {"quantity": 0, "team": "bon", "emoji": "🛡️"},
}

# Emojis de configuration et de rôles
ROLE_EMOJIS = {
    "🐺": "Loup-Garou",
    "🔮": "Voyante",
    "👨‍🌾": "Villageois",
    "🧙‍♀️": "Sorcière",
    "💘": "Cupidon",
    "🏹": "Chasseur",
    "🪶": "Corbeau",
    "🛡️": "Garde",
}

# Emojis de gestion de config
INCREASE = "➕"
DECREASE = "➖"
VALIDATE = "✅"

PHASE_TIMEOUTS = {"role_action": 90, "day": 180}
