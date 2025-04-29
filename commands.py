# commands.py

from discord.ext import commands
import state
import game
from utils import create_embed

def setup_commands(bot):
    @bot.command()
    async def start(ctx):
        """Démarre une partie."""
        await game.start_game(ctx)

    @bot.command()
    async def lock(ctx):
        """Verrouille les inscriptions et prépare la distribution des rôles."""
        if not state.join_message:
            await ctx.send(embed=create_embed("Erreur", "Aucune partie en cours d'attente de joueurs."))
            return

        state.join_locked = True
        fetched = await ctx.channel.fetch_message(state.join_message.id)
        state.join_users.extend([user async for user in fetched.reactions[0].users() if not user.bot])

        await ctx.send(embed=create_embed("Verrouillage", f"{len(state.join_users)} joueurs ont rejoint."))

    @bot.command()
    async def stop(ctx):
        """Arrête la partie actuelle."""
        await game.end_game(ctx)

    @bot.command()
    async def vote(ctx, joueur: commands.MemberConverter):
        """Vote pour lyncher un joueur pendant la phase de jour."""
        if state.current_phase == 'day' and ctx.author in state.players and joueur in state.players:
            state.votes[ctx.author] = joueur
            await ctx.send(embed=create_embed("Vote", f"{ctx.author.display_name} a voté contre {joueur.display_name}."))

    @bot.command()
    async def lg_vote(ctx, joueur: commands.MemberConverter):
        """Les Loups-Garous votent leur victime pendant la nuit."""
        if state.current_phase != 'night':
            await ctx.send(embed=create_embed("Erreur", "Ce n'est pas la phase de nuit."))
            return
        if ctx.author not in state.players or state.players[ctx.author] != 'Loup-Garou' or ctx.author in state.dead_players:
            await ctx.send(embed=create_embed("Erreur", "Vous n'êtes pas un Loup-Garou vivant."))
            return
        if joueur not in state.players or joueur in state.dead_players:
            await ctx.send(embed=create_embed("Erreur", "Cible invalide pour l'attaque."))
            return

        state.wolf_votes[ctx.author] = joueur
        await ctx.send(embed=create_embed("Vote Loup-Garou", f"{ctx.author.display_name} a voté contre {joueur.display_name}."))

    @bot.command()
    async def voir_role(ctx, joueur: commands.MemberConverter):
        """La Voyante inspecte un joueur pendant la nuit."""
        if ctx.author != state.voyante or state.vision_used or state.current_phase != 'night':
            await ctx.send(embed=create_embed("Erreur", "Vous ne pouvez pas utiliser votre voyance maintenant."))
            return
        if joueur not in state.players:
            await ctx.send(embed=create_embed("Erreur", "Ce joueur n'est pas en jeu."))
            return

        state.vision_used = True
        await ctx.send(embed=create_embed("Voyance", f"{joueur.display_name} est **{state.players[joueur]}**."))

    @bot.command()
    async def sauver(ctx):
        """La Sorcière utilise sa potion de soin."""
        if ctx.author != state.sorciere or state.witch_heal_used or state.current_phase != 'night':
            await ctx.send(embed=create_embed("Erreur", "Vous ne pouvez pas utiliser la potion de soin maintenant."))
            return

        state.victim_of_wolves = None
        state.witch_heal_used = True
        await ctx.send(embed=create_embed("Sorcière", "Vous avez utilisé votre potion de soin pour sauver la victime."))

    @bot.command()
    async def tuer(ctx, joueur: commands.MemberConverter):
        """La Sorcière utilise sa potion de poison."""
        if ctx.author != state.sorciere or state.witch_kill_used or state.current_phase != 'night':
            await ctx.send(embed=create_embed("Erreur", "Vous ne pouvez pas utiliser la potion de poison maintenant."))
            return
        if joueur not in state.players or joueur in state.dead_players:
            await ctx.send(embed=create_embed("Erreur", "Cible invalide."))
            return

        state.victim_of_witch = joueur
        state.witch_kill_used = True
        await ctx.send(embed=create_embed("Sorcière", f"Vous avez décidé d'empoisonner {joueur.display_name}."))
