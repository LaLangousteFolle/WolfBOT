# commands/general.py

import discord
from discord.ext import commands
from discord import app_commands
import game

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="start", description="Démarre la partie")
    async def start(self, interaction: discord.Interaction):
        await game.start_game(interaction)

    @app_commands.command(name="lock", description="Verrouille les inscriptions")
    async def lock(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await game.lock_game(interaction)

    @app_commands.command(name="stop", description="Arrête la partie")
    async def stop(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await game.end_game(interaction)

async def setup(bot):
    await bot.add_cog(General(bot))
