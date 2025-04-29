# config.py

# IDs de tes salons
log_channel_id = 123456789012345678
wolf_channel_id = 123456789012345678
seer_channel_id = 123456789012345678
witch_channel_id = 123456789012345678
voice_channel_id = 123456789012345678

# Configuration des rôles
ROLES_CONFIG = {
    'Loup-Garou': {'quantity': 1, 'team': 'mal', 'emoji': '🐺'},
    'Voyante': {'quantity': 1, 'team': 'bon', 'emoji': '🔮'},
    'Sorcière': {'quantity': 1, 'team': 'bon', 'emoji': '🧙‍♀️'},
    'Villageois': {'quantity': 0, 'team': 'bon', 'emoji': '👨‍🌾'}
}

PHASE_TIMEOUTS = {
    'role_action': 90,
    'day': 180
}
