import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive
import asyncio

# Charger les variables d'environnement
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Intents nécessaires
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

async def bot_main():
    await bot.load_extension("commands.general")
    await bot.load_extension("commands.vote")
    await bot.load_extension("commands.roles")
    try:
        print("🔐 TOKEN =", BOT_TOKEN)
        await bot.start(BOT_TOKEN)
    except Exception as e:
        print(f"❌ Le bot a crashé : {e}")
        import time
        while True:
            time.sleep(60)  # boucle infinie de secours

if __name__ == "__main__":
    keep_alive()
    asyncio.run(bot_main())
