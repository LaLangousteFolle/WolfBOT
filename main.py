# main.py

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
import asyncio

# Charger les variables d'environnement
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Intents nécessaires pour le bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.reactions = True
intents.message_content = True

# Initialiser le bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} commandes slash synchronisées.")
    except Exception as e:
        print(f"❌ Erreur de synchronisation des slash commands : {e}")

async def main():
    async with bot:
        # Charger toutes les extensions (commandes)
        await bot.load_extension("commands.general")  # général (start, lock, stop)
        await bot.load_extension("commands.vote")      # vote de jour/nuit
        await bot.load_extension("commands.roles")     # pouvoirs spéciaux
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    keep_alive()  # Garde le bot vivant sur Railway
    asyncio.run(main())
