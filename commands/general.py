# commands/general.py

import discord
from discord.ext import commands
from discord import app_commands
import game
import state
from utils import create_embed

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="start", description="Démarre la partie de Loups-Garous.")
    async def start(self, interaction: discord.Interaction):
        if state.game_active:
            await interaction.response.send_message("❌ Une partie est déjà en cours.", ephemeral=True)
            return
        await interaction.response.defer()
        await game.start_game(interaction)

    @app_commands.command(name="lock", description="Verrouille les inscriptions.")
    async def lock(self, interaction: discord.Interaction):
        if not state.join_message:
            await interaction.response.send_message("❌ Aucun message d'inscription détecté.", ephemeral=True)
            return
        await interaction.response.defer()
        await game.lock_game(interaction)

    @app_commands.command(name="stop", description="Arrête la partie en cours.")
    async def stop(self, interaction: discord.Interaction):
        if not state.game_active:
            await interaction.response.send_message("❌ Aucune partie n'est en cours.", ephemeral=True)
            return
        await interaction.response.defer()
        await game.end_game(interaction)

async def setup(bot):
    await bot.add_cog(General(bot))
