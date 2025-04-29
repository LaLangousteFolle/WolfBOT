# config.py
import os

# IDs de tes salons
log_channel_id = 1366109644707070032
wolf_channel_id = 1365955043215278111
seer_channel_id = 1366063228240789584
witch_channel_id = 1366063263996973077
voice_channel_id = 1366017756171866203
cupidon_channel_id = 1366699130071547955
amoureux_channel_id = 1366699189941305354

# Configuration des rôles
ROLES_CONFIG = {
    'Loup-Garou': {'quantity': 1, 'team': 'mal', 'emoji': '🐺'},
    'Voyante': {'quantity': 1, 'team': 'bon', 'emoji': '🔮'},
    'Villageois': {'quantity': 0, 'team': 'bon', 'emoji': '👨‍🌾'},
    'Sorcière': {'quantity': 1, 'team': 'bon', 'emoji': '🧙‍♀️'},
    'Cupidon': {'quantity': 1, 'team': 'bon', 'emoji': '💘'},
    'Chasseur': {'quantity': 1, 'team': 'bon', 'emoji': '🏹'}
}

PHASE_TIMEOUTS = {
    'role_action': 90,
    'day': 180
}
