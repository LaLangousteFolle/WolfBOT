# commands/vote.py

import discord
from discord import app_commands
from discord.ext import commands
import state
import game
from utils import create_embed

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="vote", description="Votez pour éliminer un joueur.")
    async def vote(self, interaction: discord.Interaction, joueur: discord.Member):
        if not state.game_active or state.current_phase != 'day':
            await interaction.response.send_message("Ce n'est pas le moment de voter.", ephemeral=True)
            return
        if interaction.user not in state.players:
            await interaction.response.send_message("Vous n'êtes pas en jeu.", ephemeral=True)
            return
        if joueur not in state.players or joueur in state.dead_players:
            await interaction.response.send_message("Cible invalide.", ephemeral=True)
            return

        state.votes[interaction.user] = joueur
        await interaction.response.send_message(f"✅ Vous avez voté contre {joueur.display_name}.")

    @app_commands.command(name="lg_vote", description="(Loups) Votez pour attaquer un joueur la nuit.")
    async def lg_vote(self, interaction: discord.Interaction, joueur: discord.Member):
        if not state.game_active or state.current_phase != 'night':
            await interaction.response.send_message("Ce n'est pas la nuit ou la partie n'est pas active.", ephemeral=True)
            return
        if interaction.user not in state.players or state.players[interaction.user] != 'Loup-Garou' or interaction.user in state.dead_players:
            await interaction.response.send_message("Vous n'êtes pas un Loup-Garou vivant.", ephemeral=True)
            return
        if joueur not in state.players or joueur in state.dead_players:
            await interaction.response.send_message("Cible invalide.", ephemeral=True)
            return

        state.wolf_votes[interaction.user] = joueur
        await interaction.response.send_message(f"🐺 Vous avez choisi {joueur.display_name} comme cible.")

async def setup(bot):
    await bot.add_cog(Vote(bot))
