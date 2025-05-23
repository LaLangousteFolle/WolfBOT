# utils.py

import discord
from datetime import datetime
import state
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
    state.guild = guild
    state.log_channel = guild.get_channel(log_channel_id)
    state.wolf_channel = guild.get_channel(wolf_channel_id)
    state.seer_channel = guild.get_channel(seer_channel_id)
    state.witch_channel = guild.get_channel(witch_channel_id)
    state.voice_channel = guild.get_channel(voice_channel_id)
    state.corbeau_channel = guild.get_channel(corbeau_channel_id)

    if not all(
        [
            state.log_channel,
            state.wolf_channel,
            state.seer_channel,
            state.witch_channel,
            state.voice_channel,
        ]
    ):
        raise ValueError("Erreur d'ID de salon.")

    await state.wolf_channel.set_permissions(guild.default_role, read_messages=False)
    await state.seer_channel.set_permissions(guild.default_role, read_messages=False)
    await state.witch_channel.set_permissions(guild.default_role, read_messages=False)
    await state.corbeau_channel.set_permissions(guild.default_role, read_messages=False)


async def mute_voice_channel():
    if state.voice_channel:
        for member in state.voice_channel.members:
            await member.edit(mute=True)


async def unmute_voice_channel():
    if state.voice_channel:
        for member in state.voice_channel.members:
            await member.edit(mute=False)


async def remove_channel_permissions(player):
    await state.wolf_channel.set_permissions(player, overwrite=None)
    await state.seer_channel.set_permissions(player, overwrite=None)
    await state.witch_channel.set_permissions(player, overwrite=None)
