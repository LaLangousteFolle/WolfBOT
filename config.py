# config.py
import os
BOT_TOKEN = os.getenv('BOT_TOKEN')

# IDs de tes salons
log_channel_id = 123456789012345678
wolf_channel_id = 123456789012345678
seer_channel_id = 123456789012345678
witch_channel_id = 123456789012345678
voice_channel_id = 123456789012345678
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
