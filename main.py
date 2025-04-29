# main.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from commands import setup_commands
from keep_alive import keep_alive

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

setup_commands(bot)
keep_alive()
bot.run(BOT_TOKEN)
