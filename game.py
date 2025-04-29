# game.py

import asyncio
import random
import state
from utils import create_embed, init_channels, mute_voice_channel, unmute_voice_channel, remove_channel_permissions
from config import ROLES_CONFIG, PHASE_TIMEOUTS

async def start_game(ctx):
    if state.game_active:
        await ctx.send(embed=create_embed("Erreur", "Une partie est déjà en cours."))
        return

    state.game_active = True
    state.vote_lock = asyncio.Lock()
    state.players.clear()
    state.votes.clear()
    state.wolf_votes.clear()
    state.dead_players.clear()
    state.join_locked = False
    state.join_users.clear()

    state.join_message = await ctx.send(embed=create_embed("Début de Partie", "Réagissez avec ✅ pour rejoindre !"))
    await state.join_message.add_reaction("✅")

    await asyncio.sleep(30)
    await lock_players(ctx)

async def lock_players(ctx):
    fetched = await ctx.channel.fetch_message(state.join_message.id)
    state.join_users.extend([user async for user in fetched.reactions[0].users() if not user.bot])

    random.shuffle(state.join_users)
    roles = [role for role, config in ROLES_CONFIG.items() for _ in range(config['quantity'])]
    random.shuffle(roles)

    for member, role in zip(state.join_users, roles):
        state.players[member] = role

    await init_channels(ctx.guild)
    await ctx.send(embed=create_embed("Distribution", "Les rôles ont été attribués."))

    await night_phase(ctx)

async def night_phase(ctx):
    state.current_phase = 'night'
    state.vision_used = False
    state.victim_of_wolves = None
    state.victim_of_witch = None
    state.wolf_votes.clear()

    await mute_voice_channel()

    await voyante_phase(ctx)
    await loups_phase(ctx)
    await sorciere_phase(ctx)

    await resolve_night(ctx)

async def voyante_phase(ctx):
    if state.voyante and state.voyante not in state.dead_players:
        await state.seer_channel.send(embed=create_embed("Voyante", f"{state.voyante.mention}, utilisez `!voir_role @joueur`."))

        await asyncio.sleep(PHASE_TIMEOUTS['role_action'] // 2)
        await state.seer_channel.send(embed=create_embed("⏰ Temps restant", "Il vous reste 45 secondes pour votre voyance."))

        await asyncio.sleep(PHASE_TIMEOUTS['role_action'] // 2)
        if not state.vision_used:
            await state.seer_channel.send(embed=create_embed("⏰ Fin du temps", "Vous n'avez pas utilisé votre pouvoir cette nuit."))

async def loups_phase(ctx):
    await state.wolf_channel.send(embed=create_embed("Loups-Garous", "Discutez et votez avec `!lg_vote @joueur`."))

    await asyncio.sleep(PHASE_TIMEOUTS['role_action'] // 2)
    await state.wolf_channel.send(embed=create_embed("⏰ Temps restant", "Il vous reste 45 secondes pour choisir votre victime."))

    await asyncio.sleep(PHASE_TIMEOUTS['role_action'] // 2)
    if not state.wolf_votes:
        await state.wolf_channel.send(embed=create_embed("⏰ Fin du temps", "Aucun vote de Loups-Garous cette nuit."))

async def sorciere_phase(ctx):
    if state.sorciere and state.sorciere not in state.dead_players:
        if state.victim_of_wolves and not state.witch_heal_used:
            await state.witch_channel.send(embed=create_embed("Sorcière", f"{state.sorciere.mention}, {state.victim_of_wolves.mention} a été attaqué. `!sauver` ou `!tuer @joueur`."))

        else:
            await state.witch_channel.send(embed=create_embed("Sorcière", f"{state.sorciere.mention}, vous pouvez utiliser `!tuer @joueur`."))

        await asyncio.sleep(PHASE_TIMEOUTS['role_action'] // 2)
        await state.witch_channel.send(embed=create_embed("⏰ Temps restant", "Il vous reste 45 secondes pour décider."))

        await asyncio.sleep(PHASE_TIMEOUTS['role_action'] // 2)
        if not state.witch_heal_used and not state.witch_kill_used:
            await state.witch_channel.send(embed=create_embed("⏰ Fin du temps", "Vous n'avez pas utilisé vos potions cette nuit."))

async def resolve_night(ctx):
    await unmute_voice_channel()

    deaths = []
    if state.victim_of_wolves and state.victim_of_wolves not in state.dead_players:
        deaths.append(state.victim_of_wolves)
    if state.victim_of_witch and state.victim_of_witch not in state.dead_players:
        deaths.append(state.victim_of_witch)

    for player in deaths:
        await remove_player(ctx, player)

    if deaths:
        names = ', '.join(p.display_name for p in deaths)
        await ctx.send(embed=create_embed("✝️ Victimes", f"Au matin, le village découvre : {names}"))
    else:
        await ctx.send(embed=create_embed("☀️ Jour", "La nuit fut calme..."))

    await day_phase(ctx)

async def day_phase(ctx):
    state.current_phase = 'day'
    await ctx.send(embed=create_embed("Vote", "Utilisez `!vote @joueur` pour désigner un coupable."))

    await asyncio.sleep(PHASE_TIMEOUTS['day'] // 2)
    await ctx.send(embed=create_embed("⏰ Temps restant", "Il vous reste 90 secondes pour voter."))

    await asyncio.sleep(PHASE_TIMEOUTS['day'] // 2)
    await end_day_phase(ctx)

async def end_day_phase(ctx):
    async with state.vote_lock:
        if state.votes:
            count = {}
            for voter, target in state.votes.items():
                count[target] = count.get(target, 0) + 1
            eliminated = max(count, key=count.get)
            await ctx.send(embed=create_embed("📩 Verdict", f"{eliminated.mention} a été éliminé par le village."))
            await remove_player(ctx, eliminated)
        else:
            await ctx.send(embed=create_embed("📩 Verdict", "Personne n'a été éliminé."))

    state.votes.clear()
    await check_game_end(ctx)

async def remove_player(ctx, player):
    if player in state.players:
        role = state.players[player]
        state.dead_players.add(player)
        del state.players[player]
        await remove_channel_permissions(player)
        await ctx.send(embed=create_embed("Révélation", f"{player.display_name} était **{role}**."))

async def check_game_end(ctx):
    roles_alive = [role for role in state.players.values()]
    if roles_alive.count('Loup-Garou') == 0:
        await ctx.send(embed=create_embed("🏆 Victoire", "Les Villageois ont gagné !"))
        await end_game(ctx)
    elif roles_alive.count('Loup-Garou') >= len(roles_alive) / 2:
        await ctx.send(embed=create_embed("🏆 Victoire", "Les Loups-Garous ont gagné !"))
        await end_game(ctx)
    else:
        await night_phase(ctx)

async def end_game(ctx):
    state.game_active = False
    await ctx.send(embed=create_embed("Fin de Partie", "La partie est terminée."))
