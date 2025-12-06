# utils.py

import discord
from datetime import datetime
from game_session import get_session
import config
from config import (
    log_channel_id,
    wolf_channel_id,
    seer_channel_id,
    witch_channel_id,
    voice_channel_id,
    corbeau_channel_id,
)


def create_embed(title, description, color=0x00FF00):
    return discord.Embed(
        title=title, description=description, color=color, timestamp=datetime.now()
    )


async def init_channels(guild):
    session = get_session(guild)
    
    # Initialisation des canaux
    session.log_channel = guild.get_channel(log_channel_id)
    session.wolf_channel = guild.get_channel(wolf_channel_id)
    session.seer_channel = guild.get_channel(seer_channel_id)
    session.witch_channel = guild.get_channel(witch_channel_id)
    session.voice_channel = guild.get_channel(voice_channel_id)
    session.corbeau_channel = guild.get_channel(corbeau_channel_id)
    session.cupidon_channel = guild.get_channel(config.cupidon_channel_id)
    session.amoureux_channel = guild.get_channel(config.amoureux_channel_id)
    session.garde_channel = guild.get_channel(config.garde_channel_id)

    # Vérification que tous les canaux ont été correctement trouvés
    missing_channels = []
    if not session.log_channel: missing_channels.append("log_channel")
    if not session.wolf_channel: missing_channels.append("wolf_channel")
    if not session.seer_channel: missing_channels.append("seer_channel")
    if not session.witch_channel: missing_channels.append("witch_channel")
    if not session.voice_channel: missing_channels.append("voice_channel")
    if not session.corbeau_channel: missing_channels.append("corbeau_channel")
    if not session.cupidon_channel: missing_channels.append("cupidon_channel")
    if not session.amoureux_channel: missing_channels.append("amoureux_channel")
    if not session.garde_channel: missing_channels.append("garde_channel")
    
    if missing_channels:
        raise ValueError(f"Erreur d'ID de salon. Canaux manquants : {', '.join(missing_channels)}")

    # Configuration des permissions des canaux
    if session.wolf_channel:
        await session.wolf_channel.set_permissions(guild.default_role, read_messages=False)
    if session.seer_channel:
        await session.seer_channel.set_permissions(guild.default_role, read_messages=False)
    if session.witch_channel:
        await session.witch_channel.set_permissions(guild.default_role, read_messages=False)
    if session.corbeau_channel:
        await session.corbeau_channel.set_permissions(guild.default_role, read_messages=False)
    if session.cupidon_channel:
        await session.cupidon_channel.set_permissions(guild.default_role, read_messages=False)
    if session.amoureux_channel:
        await session.amoureux_channel.set_permissions(guild.default_role, read_messages=False)
    if session.garde_channel:
        await session.garde_channel.set_permissions(guild.default_role, read_messages=False)


async def mute_voice_channel(guild):
    session = get_session(guild)
    if session.voice_channel:
        try:
            members = list(session.voice_channel.members)
            for member in members:
                await member.edit(mute=True)
            print("Tous les joueurs ont été rendus muets dans le canal vocal")
        except discord.Forbidden:
            print("Permissions insuffisantes pour rendre muet")
        except Exception as e:
            print(f"Erreur lors du mute: {e}")


async def unmute_voice_channel(guild):
    session = get_session(guild)
    if session.voice_channel:
        try:
            members = list(session.voice_channel.members)
            for member in members:
                await member.edit(mute=False)
            print("Tous les joueurs peuvent maintenant parler dans le canal vocal")
        except discord.Forbidden:
            print("Permissions insuffisantes pour rendre la parole")
        except Exception as e:
            print(f"Erreur lors du unmute: {e}")


async def remove_channel_permissions(player, guild):
    session = get_session(guild)
    try:
        channels = []
        if session.wolf_channel: channels.append(session.wolf_channel)
        if session.seer_channel: channels.append(session.seer_channel)
        if session.witch_channel: channels.append(session.witch_channel)
        if session.cupidon_channel: channels.append(session.cupidon_channel)
        if session.corbeau_channel: channels.append(session.corbeau_channel)
        if session.amoureux_channel: channels.append(session.amoureux_channel)
        if session.garde_channel: channels.append(session.garde_channel)
        
        for channel in channels:
            try:
                await channel.set_permissions(player, overwrite=None)
            except Exception as e:
                print(f"Erreur lors de la suppression des permissions sur un canal: {e}")
    except discord.Forbidden:
        print(f"Permissions insuffisantes pour modifier les permissions de {player.display_name}")
    except Exception as e:
        print(f"Erreur lors de la suppression des permissions: {e}")
