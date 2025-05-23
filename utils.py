# utils.py

import discord
from datetime import datetime
import state
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
    # Stockage du guild dans state
    state.guild = guild
    
    # Initialisation des canaux
    state.log_channel = guild.get_channel(log_channel_id)
    state.wolf_channel = guild.get_channel(wolf_channel_id)
    state.seer_channel = guild.get_channel(seer_channel_id)
    state.witch_channel = guild.get_channel(witch_channel_id)
    state.voice_channel = guild.get_channel(voice_channel_id)
    state.corbeau_channel = guild.get_channel(corbeau_channel_id)
    state.cupidon_channel = guild.get_channel(config.cupidon_channel_id)
    state.amoureux_channel = guild.get_channel(config.amoureux_channel_id)
    state.garde_channel = guild.get_channel(config.garde_channel_id)

    # Vérification que tous les canaux ont été correctement trouvés
    missing_channels = []
    if not state.log_channel: missing_channels.append("log_channel")
    if not state.wolf_channel: missing_channels.append("wolf_channel")
    if not state.seer_channel: missing_channels.append("seer_channel")
    if not state.witch_channel: missing_channels.append("witch_channel")
    if not state.voice_channel: missing_channels.append("voice_channel")
    if not state.corbeau_channel: missing_channels.append("corbeau_channel")
    if not state.cupidon_channel: missing_channels.append("cupidon_channel")
    if not state.amoureux_channel: missing_channels.append("amoureux_channel")
    if not state.garde_channel: missing_channels.append("garde_channel")
    
    if missing_channels:
        raise ValueError(f"Erreur d'ID de salon. Canaux manquants : {', '.join(missing_channels)}")

    # Configuration des permissions des canaux
    if state.wolf_channel:
        await state.wolf_channel.set_permissions(guild.default_role, read_messages=False)
    if state.seer_channel:
        await state.seer_channel.set_permissions(guild.default_role, read_messages=False)
    if state.witch_channel:
        await state.witch_channel.set_permissions(guild.default_role, read_messages=False)
    if state.corbeau_channel:
        await state.corbeau_channel.set_permissions(guild.default_role, read_messages=False)


async def mute_voice_channel():
    if state.voice_channel:
        try:
            members = list(state.voice_channel.members)
            for member in members:
                await member.edit(mute=True)
            print("Tous les joueurs ont été rendus muets dans le canal vocal")
        except discord.Forbidden:
            print("Permissions insuffisantes pour rendre muet")
        except Exception as e:
            print(f"Erreur lors du mute: {e}")


async def unmute_voice_channel():
    if state.voice_channel:
        try:
            members = list(state.voice_channel.members)
            for member in members:
                await member.edit(mute=False)
            print("Tous les joueurs peuvent maintenant parler dans le canal vocal")
        except discord.Forbidden:
            print("Permissions insuffisantes pour rendre la parole")
        except Exception as e:
            print(f"Erreur lors du unmute: {e}")


async def remove_channel_permissions(player):
    try:
        channels = []
        if state.wolf_channel: channels.append(state.wolf_channel)
        if state.seer_channel: channels.append(state.seer_channel)
        if state.witch_channel: channels.append(state.witch_channel)
        if state.cupidon_channel: channels.append(state.cupidon_channel)
        if state.corbeau_channel: channels.append(state.corbeau_channel)
        
        for channel in channels:
            try:
                await channel.set_permissions(player, overwrite=None)
            except Exception as e:
                print(f"Erreur lors de la suppression des permissions sur un canal: {e}")
    except discord.Forbidden:
        print(f"Permissions insuffisantes pour modifier les permissions de {player.display_name}")
    except Exception as e:
        print(f"Erreur lors de la suppression des permissions: {e}")
