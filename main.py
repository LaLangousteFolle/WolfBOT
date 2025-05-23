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
    try:
        # Chargement des extensions
        extensions = [
            "commands.general",
            "commands.vote",
            "commands.config",
            "commands.roles"
        ]
        
        for extension in extensions:
            try:
                await bot.load_extension(extension)
                print(f"✅ Extension {extension} chargée avec succès")
            except Exception as e:
                print(f"❌ Erreur lors du chargement de l'extension {extension}: {e}")
        
        # Démarrage du bot
        if BOT_TOKEN:
            token_preview = BOT_TOKEN[:5] + "..." if BOT_TOKEN else "Non défini"
            print(f"🔐 TOKEN = {token_preview}")
            await bot.start(BOT_TOKEN)
        else:
            print("❌ BOT_TOKEN non défini. Impossible de démarrer le bot.")
            return
    except Exception as e:
        print(f"❌ Le bot a crashé : {e}")
        import time
        while True:
            time.sleep(60)

if __name__ == "__main__":
    # Démarrage du serveur web pour garder le bot en vie
    keep_alive()
    
    # Démarrage du bot avec gestion d'erreurs
    try:
        asyncio.run(bot_main())
    except discord.LoginFailure:
        print("❌ Échec de connexion: Token invalide ou expiré")
    except Exception as e:
        print(f"❌ Crash de haut niveau : {e}")

    # Boucle de maintien en vie en cas de crash
    import time
    print("⚠️ Le bot s'est arrêté. Boucle de maintien active...")
    while True:
        print("🌀 Boucle de maintien active pour Railway...")
        time.sleep(60)