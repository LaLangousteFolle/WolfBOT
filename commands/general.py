# commands/general.py

import discord
from discord.ext import commands
from discord import app_commands
import game
from game_session import get_session
from utils import create_embed

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="start", description="Démarre la partie de Loups-Garous.")
    async def start(self, interaction: discord.Interaction):
        session = get_session(interaction.guild)
        if session.game_active:
            await interaction.response.send_message("❌ Une partie est déjà en cours.", ephemeral=True)
            return
        await interaction.response.defer()
        await game.start_game(interaction)

    @app_commands.command(name="lock", description="Verrouille les inscriptions.")
    async def lock(self, interaction: discord.Interaction):
        session = get_session(interaction.guild)
        if not session.join_message:
            await interaction.response.send_message("❌ Aucun message d'inscription détecté.", ephemeral=True)
            return
        await interaction.response.defer()
        await game.lock_game(interaction)

    @app_commands.command(name="stop", description="Arrête la partie en cours.")
    async def stop(self, interaction: discord.Interaction):
        session = get_session(interaction.guild)
        if not session.game_active:
            await interaction.response.send_message("❌ Aucune partie n'est en cours.", ephemeral=True)
            return
        await interaction.response.defer()
        await game.end_game(interaction.channel)

async def setup(bot):
    await bot.add_cog(General(bot))
