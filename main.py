import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Charger les variables d'environnement (.env)
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Définir les intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.reactions = True
intents.message_content = True

# Créer le bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Événement : Bot prêt
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()  # Synchroniser les slash commands
        print(f"✅ {len(synced)} commandes slash synchronisées.")
    except Exception as e:
        print(f"❌ Erreur lors de la synchro des commandes slash : {e}")

    print(f"✅ Connecté en tant que {bot.user}")

# Charger dynamiquement les Cogs
async def load_cogs():
    await bot.load_extension("commands.vote")
    await bot.load_extension("commands.roles")
    await bot.load_extension("commands.commands")

# Lancer le bot
async def main():
    await load_cogs()
    await bot.start(BOT_TOKEN)

# Point d’entrée du script
if __name__ == "__main__":
    from keep_alive import keep_alive
    keep_alive()  # Lancer Flask pour Railway
    import asyncio
    asyncio.run(main())
