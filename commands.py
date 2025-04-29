# commands.py

from discord.ext import commands
import state
import game
from utils import create_embed

def setup_commands(bot):
    @bot.command()
    async def start(ctx):
        await game.start_game(ctx)

    @bot.command()
    async def stop(ctx):
        await game.end_game(ctx)

    @bot.command()
    async def vote(ctx, joueur: commands.MemberConverter):
        if state.current_phase == 'day' and ctx.author in state.players and joueur in state.players:
            state.votes[ctx.author] = joueur
            await ctx.send(embed=create_embed("Vote", f"{ctx.author.display_name} a voté contre {joueur.display_name}"))
