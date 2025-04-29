# commands.py

from discord.ext import commands
import state
import game
from utils import create_embed

def setup_commands(bot):
    @bot.command()
    async def start(ctx):
        """Commence la phase d'inscription des joueurs."""
        if state.game_active:
            await ctx.send(embed=create_embed("Erreur", "Une partie est déjà en cours."))
            return

        state.game_active = True
        state.players.clear()
        state.join_users.clear()
        state.dead_players.clear()
        state.votes.clear()
        state.join_locked = False

        join_msg = await ctx.send(embed=create_embed(
            "🎉 Nouvelle Partie",
            "Réagissez avec ✅ pour rejoindre la partie !\nQuand tout le monde est prêt, tapez `!lock`."
        ))
        state.join_message = join_msg
        await join_msg.add_reaction("✅")


    @bot.command()
    async def lock(ctx):
        """Verrouille les inscriptions et lance la distribution des rôles."""
        if not state.join_message:
            await ctx.send(embed=create_embed("Erreur", "Aucune partie en cours d'attente de joueurs."))
            return

        state.join_locked = True
        fetched = await ctx.channel.fetch_message(state.join_message.id)
        players = [user async for user in fetched.reactions[0].users() if not user.bot]

        if len(players) < 2:
            await ctx.send(embed=create_embed("Erreur", "Pas assez de joueurs pour démarrer."))
            state.game_active = False
            return

        state.join_users = players
        await ctx.send(embed=create_embed("Verrouillage", f"{len(state.join_users)} joueurs ont rejoint."))
        
        # Maintenant on lance la vraie partie
        await game.start_game(ctx)

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
        
    @bot.command()
    async def choisir(ctx, joueur1: commands.MemberConverter, joueur2: commands.MemberConverter):
        """Cupidon choisit deux amoureux."""
        if ctx.author != state.cupidon or state.current_phase != 'night':
            await ctx.send(embed=create_embed("Erreur", "Vous n'avez pas le droit d'utiliser cette commande."))
            return
        if joueur1 == joueur2 or joueur1 not in state.players or joueur2 not in state.players:
            await ctx.send(embed=create_embed("Erreur", "Sélection invalide."))
            return

        state.amoureux_pair = [joueur1, joueur2]

        await state.amoureux_channel.set_permissions(joueur1, read_messages=True, send_messages=True, add_reactions=True)
        await state.amoureux_channel.set_permissions(joueur2, read_messages=True, send_messages=True, add_reactions=True)

        await state.cupidon_channel.send(embed=create_embed(
            "Cupidon", f"💘 {joueur1.display_name} et {joueur2.display_name} sont désormais liés par l'amour éternel."
        ))

    @bot.command()
    async def tirer(ctx, joueur: commands.MemberConverter):
        """Le Chasseur tire après sa mort."""
        if ctx.author != state.tir_cible:
            await ctx.send(embed=create_embed("Erreur", "Vous n'avez pas le droit de tirer."))
            return
        if joueur not in state.players or joueur in state.dead_players:
            await ctx.send(embed=create_embed("Erreur", "Cible invalide."))
            return

        await ctx.send(embed=create_embed("🏹 Dernière flèche", f"{ctx.author.display_name} tire et tue {joueur.display_name} avant de mourir."))
        await game.remove_player(ctx, joueur)
        state.tir_cible = None  # Reset
