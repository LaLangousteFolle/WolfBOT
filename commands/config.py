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

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_config = {"message": None, "user": None}

    @app_commands.command(name="config", description="Configurer les rôles de la partie avant de commencer.")
    async def config_command(self, interaction: discord.Interaction):
        self.temp_config["user"] = interaction.user
        embed = self.build_config_embed()
        msg = await interaction.channel.send(embed=embed)
        self.temp_config["message"] = msg

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

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        if self.temp_config["message"] is None or reaction.message.id != self.temp_config["message"].id:
            return
        if user != self.temp_config["user"]:
            return

        emoji_used = str(reaction.emoji)

        # Valider
        if emoji_used == VALIDATE:
            await self.temp_config["message"].channel.send("✅ Configuration terminée. Vous pouvez maintenant lancer la partie avec /start")
            return

        # Identifier le rôle lié à la ligne réagie
        lines = self.temp_config["message"].embeds[0].description.split("\n")
        for line in lines:
            for emoji, role in ROLE_EMOJIS.items():
                if emoji in line:
                    if emoji_used == INCREASE:
                        config.ROLES_CONFIG[role]["quantity"] += 1
                    elif emoji_used == DECREASE and config.ROLES_CONFIG[role]["quantity"] > 0:
                        config.ROLES_CONFIG[role]["quantity"] -= 1
                    new_embed = self.build_config_embed()
                    await self.temp_config["message"].edit(embed=new_embed)
                    return

async def setup(bot):
    await bot.add_cog(Config(bot))
