# commands/config.py

import discord
from discord.ext import commands
from discord import app_commands
import config
from utils import create_embed

ROLE_EMOJIS = {
    "🐺": "Loup-Garou",
    "🔮": "Voyante",
    "👨‍🌾": "Villageois",
    "🧙‍♀️": "Sorcière",
    "💘": "Cupidon",
    "🏹": "Chasseur",
}
INCREASE = "➕"
DECREASE = "➖"
VALIDATE = "✅"

temp_config = {"message": None, "user": None}

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="config", description="Configurer les rôles de la partie avant de commencer.")
    async def config(self, interaction: discord.Interaction):
        temp_config["user"] = interaction.user
        embed = self.build_config_embed()
        msg = await interaction.channel.send(embed=embed)
        temp_config["message"] = msg

        for emoji in ROLE_EMOJIS:
            await msg.add_reaction(emoji)
        await msg.add_reaction(INCREASE)
        await msg.add_reaction(DECREASE)
        await msg.add_reaction(VALIDATE)

        await interaction.response.send_message("🛠 Configuration en cours...", ephemeral=True)

    def build_config_embed(self):
        lines = []
        for role, data in config.ROLES_CONFIG.items():
            emoji = data['emoji']
            qty = data['quantity']
            lines.append(f"{emoji} **{role}** : {qty}")
        return create_embed("⚙️ Configuration des rôles", "\n".join(lines))

async def setup(bot):
    await bot.add_cog(Config(bot))
