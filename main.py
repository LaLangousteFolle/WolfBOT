# main.py
import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from commands import setup_commands
from keep_alive import keep_alive

load_dotenv()  # ← Important pour charger .env

BOT_TOKEN = os.getenv("BOT_TOKEN")  # ← Charger la variable d'environnement

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def main():
    async with bot:
        setup_commands(bot)
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())


@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

setup_commands(bot)

keep_alive()
bot.run(BOT_TOKEN)