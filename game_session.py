# game_session.py
import asyncio
from typing import Dict, Set, List, Optional
import discord

class GameSession:
    
    def __init__(self, guild: discord.Guild):
        self.guild = guild
        self.game_active = False
        self.current_phase = None
        
        self.players: Dict[discord.Member, str] = {}  # {member: role}
        self.dead_players: Set[discord.Member] = set()
        self.join_users: List[discord.Member] = []
        self.join_locked = False
        self.join_message: Optional[discord.Message] = None
        
        self.votes: Dict[discord.Member, discord.Member] = {}
        self.wolf_votes: Dict[discord.Member, discord.Member] = {}
        
        self.voyante: Optional[discord.Member] = None
        self.sorciere: Optional[discord.Member] = None
        self.cupidon: Optional[discord.Member] = None
        self.chasseur: Optional[discord.Member] = None
        self.corbeau: Optional[discord.Member] = None
        self.garde: Optional[discord.Member] = None
        
        self.amoureux_pair: List[discord.Member] = []
        self.corbeau_target: Optional[discord.Member] = None
        
        self.log_channel: Optional[discord.TextChannel] = None
        self.wolf_channel: Optional[discord.TextChannel] = None
        self.seer_channel: Optional[discord.TextChannel] = None
        self.witch_channel: Optional[discord.TextChannel] = None
        self.voice_channel: Optional[discord.VoiceChannel] = None
        self.cupidon_channel: Optional[discord.TextChannel] = None
        self.amoureux_channel: Optional[discord.TextChannel] = None
        self.corbeau_channel: Optional[discord.TextChannel] = None
        self.garde_channel: Optional[discord.TextChannel] = None
        
        self.witch_heal_used = False
        self.witch_kill_used = False
        self.vision_used = False
        
        # victimes
        self.victim_of_wolves: Optional[discord.Member] = None
        self.victim_of_witch: Optional[discord.Member] = None
        
        # garde
        self.last_protected: Optional[discord.Member] = None
        self.protected_tonight: Optional[discord.Member] = None
        
        # chasseur
        self.tir_cible: Optional[discord.Member] = None
        
        self.vote_event = asyncio.Event()
        self.action_events: Dict[str, asyncio.Event] = {
            'cupidon': asyncio.Event(),
            'voyante': asyncio.Event(),
            'garde': asyncio.Event(),
            'witch': asyncio.Event(),
            'wolves': asyncio.Event(),
        }
    
    def reset(self):
        self.__init__(self.guild)
    
    def is_alive(self, member: discord.Member) -> bool:
        return member in self.players and member not in self.dead_players
    
    def get_living_players(self) -> List[discord.Member]:
        return [p for p in self.players if p not in self.dead_players]
    
    def get_role(self, member: discord.Member) -> Optional[str]:
        return self.players.get(member)


# Gestionnaire global des sessions (une par serveur)
_sessions: Dict[int, GameSession] = {}

def get_session(guild: discord.Guild) -> GameSession:
    if guild.id not in _sessions:
        _sessions[guild.id] = GameSession(guild)
    return _sessions[guild.id]

def reset_session(guild: discord.Guild):
    if guild.id in _sessions:
        _sessions[guild.id].reset()

