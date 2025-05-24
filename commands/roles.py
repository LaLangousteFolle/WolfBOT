# commands/roles.py

import discord
from discord import app_commands
from discord.ext import commands
import state
import game
import utils
from utils import *


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="voir_role", description="(Voyante) Inspectez le rôle d'un joueur."
    )
    async def voir_role(self, interaction: discord.Interaction, joueur: discord.Member):
        if (
            interaction.user != state.voyante
            or state.vision_used
            or state.current_phase != "night"
        ):
            await interaction.response.send_message(
                "Vous ne pouvez pas utiliser votre pouvoir maintenant.", ephemeral=True
            )
            return
        if joueur not in state.players:
            await interaction.response.send_message(
                "Ce joueur n'est pas en jeu.", ephemeral=True
            )
            return

        state.vision_used = True
        await interaction.response.send_message(
            f"🔮 {joueur.display_name} est **{state.players[joueur]}**."
        )

    @app_commands.command(
        name="sauver", description="(Sorcière) Sauvez la victime de la nuit."
    )
    async def sauver(self, interaction: discord.Interaction):
        if (
            interaction.user != state.sorciere
            or state.witch_heal_used
            or state.current_phase != "night"
        ):
            await interaction.response.send_message(
                "Vous ne pouvez pas utiliser la potion de soin maintenant.",
                ephemeral=True,
            )
            return

        state.victim_of_wolves = None
        state.witch_heal_used = True
        await interaction.response.send_message(
            "🧙‍♀️ Vous avez utilisé votre potion de soin pour sauver la victime."
        )

    @app_commands.command(
        name="tuer",
        description="(Sorcière) Tuez un joueur avec votre potion de poison.",
    )
    async def tuer(self, interaction: discord.Interaction, joueur: discord.Member):
        if (
            interaction.user != state.sorciere
            or state.witch_kill_used
            or state.current_phase != "night"
        ):
            await interaction.response.send_message(
                "Vous ne pouvez pas utiliser la potion de poison maintenant.",
                ephemeral=True,
            )
            return
        if joueur not in state.players or joueur in state.dead_players:
            await interaction.response.send_message("Cible invalide.", ephemeral=True)
            return

        state.victim_of_witch = joueur
        state.witch_kill_used = True
        await interaction.response.send_message(
            f"☠️ Vous avez choisi d'empoisonner {joueur.display_name}."
        )

    @app_commands.command(
        name="choisir", description="(Cupidon) Choisissez deux amoureux."
    )
    async def choisir(
        self,
        interaction: discord.Interaction,
        joueur1: discord.Member,
        joueur2: discord.Member,
    ):
        if interaction.user != state.cupidon or state.current_phase != "cupidon":
            await interaction.response.send_message(
                "Vous ne pouvez pas utiliser cette commande maintenant.", ephemeral=True
            )
            return
        if (
            joueur1 == joueur2
            or joueur1 not in state.players
            or joueur2 not in state.players
        ):
            await interaction.response.send_message(
                "Sélection invalide.", ephemeral=True
            )
            return

        state.amoureux_pair = [joueur1, joueur2]

        try:
            if state.amoureux_channel:
                try:
                    await state.amoureux_channel.set_permissions(
                        joueur1, read_messages=True, send_messages=True, add_reactions=True
                    )
                    await state.amoureux_channel.set_permissions(
                        joueur2, read_messages=True, send_messages=True, add_reactions=True
                    )
                except Exception as e:
                    print(f"Erreur lors de la définition des permissions: {e}")
        except Exception as e:
            print(f"Erreur lors de la configuration des permissions des amoureux: {e}")

        await interaction.response.send_message(
            f"💘 {joueur1.display_name} et {joueur2.display_name} sont désormais liés pour la vie !"
        )

    @app_commands.command(
        name="tirer",
        description="(Chasseur) Tirez une dernière balle après votre mort.",
    )
    async def tirer(self, interaction: discord.Interaction, joueur: discord.Member):
        if interaction.user != state.tir_cible:
            await interaction.response.send_message(
                "Vous ne pouvez pas tirer.", ephemeral=True
            )
            return
        if joueur not in state.players or joueur in state.dead_players:
            await interaction.response.send_message("Cible invalide.", ephemeral=True)
            return

        await interaction.response.send_message(
            f"🏹 Vous avez tué {joueur.display_name} avant de mourir !"
        )
        await game.remove_player(interaction, joueur)
        state.tir_cible = None

    @app_commands.command(
        name="marquer",
        description="(Corbeau) Marquez un joueur pour lui infliger un malus de votes.",
    )
    async def marquer(self, interaction: discord.Interaction, joueur: discord.Member):
        if interaction.user != state.corbeau or state.current_phase != "night":
            await interaction.response.send_message(
                "Vous ne pouvez pas utiliser cette commande maintenant.", ephemeral=True
            )
            return
        if joueur not in state.players or joueur in state.dead_players:
            await interaction.response.send_message("Cible invalide.", ephemeral=True)
            return

        state.corbeau_target = joueur
        await interaction.response.send_message(
            f"🪶 Vous avez marqué {joueur.display_name}. Il recevra un malus au prochain vote."
        )

    @app_commands.command(
        name="proteger", description="(Garde) Protégez un joueur pendant la nuit."
    )
    async def proteger(self, interaction: discord.Interaction, joueur: discord.Member):
        if interaction.user != state.garde or state.current_phase != "night":
            await interaction.response.send_message(
                "Vous ne pouvez pas utiliser cette commande maintenant.", ephemeral=True
            )
            return
        if joueur == state.last_protected:
            await interaction.response.send_message(
                "⛔ Vous ne pouvez pas protéger deux fois de suite la même personne.",
                ephemeral=True,
            )
            return
        if joueur not in state.players or joueur in state.dead_players:
            await interaction.response.send_message("Cible invalide.", ephemeral=True)
            return

        state.protected_tonight = joueur
        await interaction.response.send_message(
            f"🛡️ Vous avez choisi de protéger {joueur.display_name} cette nuit."
        )


async def setup(bot):
    await bot.add_cog(Roles(bot))
