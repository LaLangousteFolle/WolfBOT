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

    @app_commands.command(
        name="config",
        description="Configurer les rôles de la partie avant de commencer.",
    )
    async def config_command(self, interaction: discord.Interaction):
        try:
            # Stockage des données de configuration temporaires
            self.config_data = {
                "user": interaction.user,
                "message": None
            }
            
            # Création de l'embed de configuration
            embed = self.build_config_embed()
            
            # Envoi du message de configuration
            if hasattr(interaction, 'channel') and interaction.channel and hasattr(interaction.channel, 'send'):
                msg = await interaction.channel.send(embed=embed)
                self.config_data["message"] = msg

                # Ajout des réactions
                for emoji in ROLE_EMOJIS:
                    await msg.add_reaction(emoji)
                await msg.add_reaction(INCREASE)
                await msg.add_reaction(DECREASE)
                await msg.add_reaction(VALIDATE)

                # Confirmation à l'utilisateur
                await interaction.response.send_message(
                    "🛠 Configuration en cours...", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "❌ Erreur: Impossible d'accéder au canal", ephemeral=True
                )
        except Exception as e:
            print(f"Erreur lors de la configuration: {e}")
            await interaction.response.send_message(
                "❌ Une erreur s'est produite lors de la configuration.", ephemeral=True
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