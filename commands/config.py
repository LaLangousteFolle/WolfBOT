# commands/config.py

import discord
from discord.ext import commands
from discord import app_commands
import config
from config import ROLE_EMOJIS, INCREASE, DECREASE, VALIDATE
from utils import create_embed


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_data = {}

    @app_commands.command(name="config", description="Configurer les rôles via saisie utilisateur.")
    async def config_command(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        user = interaction.user

        def check(m):
            return m.author == user and m.channel == interaction.channel

        for role, data in config.ROLES_CONFIG.items():
            await interaction.followup.send(
                f"Combien de **{role}** {data['emoji']} ? (réponds par un nombre entier)"
            )
            try:
                msg = await self.bot.wait_for("message", timeout=60.0, check=check)
                quantity = int(msg.content)
                config.ROLES_CONFIG[role]["quantity"] = max(0, quantity)
            except (discord.errors.NotFound, ValueError, TimeoutError):
                await interaction.followup.send(f"⏱️ Entrée invalide. Valeur par défaut : 0 pour {role}")
                config.ROLES_CONFIG[role]["quantity"] = 0

        await interaction.followup.send("✅ Configuration terminée. Tu peux lancer la partie avec `/start`.")

        summary = "\n".join(
            f"{data['emoji']} **{role}** : {data['quantity']}"
            for role, data in config.ROLES_CONFIG.items()
        )
        await interaction.followup.send(
            embed=discord.Embed(
                title="📋 Configuration actuelle",
                description=summary,
                color=0x00ffcc
            )
        )
    def build_config_embed(self):
        lines = []
        for role, data in config.ROLES_CONFIG.items():
            emoji = data["emoji"]
            qty = data["quantity"]
            lines.append(f"{emoji} **{role}** : {qty}")
        return create_embed("⚙️ Configuration des rôles", "\n".join(lines))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Ignorer les réactions des bots
        if user.bot:
            return

        # Vérifier si c'est une réaction sur notre message de configuration
        if not self.config_data.get("message"):
            return
        if reaction.message.id != self.config_data["message"].id:
            return
        if user != self.config_data.get("user"):
            return

        emoji_used = str(reaction.emoji)

        # Traitement de la validation
        if emoji_used == VALIDATE:
            try:
                channel = reaction.message.channel
                if channel and hasattr(channel, 'send'):
                    await channel.send(
                        "✅ Configuration terminée. Vous pouvez maintenant lancer la partie avec /start"
                    )
            except Exception as e:
                print(f"Erreur lors de l'envoi du message de configuration terminée: {e}")
            return

        # Chercher le rôle correspondant à l'emoji utilisé
        try:
            message = self.config_data.get("message")
            if not message or not message.embeds:
                return

            description = message.embeds[0].description
            if not description:
                return

            lines = description.split("\n")

            # Traitement des modifications de quantité
            for line in lines:
                for emoji, role_name in ROLE_EMOJIS.items():
                    if emoji in line and role_name in config.ROLES_CONFIG:
                        if emoji_used == INCREASE:
                            config.ROLES_CONFIG[role_name]["quantity"] += 1
                            await self.update_config_embed()
                            return
                        elif (
                            emoji_used == DECREASE
                            and config.ROLES_CONFIG[role_name]["quantity"] > 0
                        ):
                            config.ROLES_CONFIG[role_name]["quantity"] -= 1
                            await self.update_config_embed()
                            return
        except Exception as e:
            print(f"Erreur lors du traitement de la réaction: {e}")

    async def update_config_embed(self):
        try:
            message = self.config_data.get("message")
            if message:
                new_embed = self.build_config_embed()
                await message.edit(embed=new_embed)
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'embed: {e}")


async def setup(bot):
    await bot.add_cog(Config(bot))
