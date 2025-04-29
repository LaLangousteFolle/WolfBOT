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
    await ctx.send(embed=create_embed("Distribution", "Les rôles sont attribués."))

    await night_phase(ctx)

async def night_phase(ctx):
    state.current_phase = 'night'
    await mute_voice_channel()
    await asyncio.sleep(PHASE_TIMEOUTS['role_action'])
    await unmute_voice_channel()
    await day_phase(ctx)

async def day_phase(ctx):
    state.current_phase = 'day'
    await ctx.send(embed=create_embed("Vote", "Utilisez `!vote @joueur` pour voter."))
    await asyncio.sleep(PHASE_TIMEOUTS['day'])
    await end_day_phase(ctx)

async def end_day_phase(ctx):
    async with state.vote_lock:
        if state.votes:
            count = {}
            for voter, target in state.votes.items():
                count[target] = count.get(target, 0) + 1
            eliminated = max(count, key=count.get)
            await ctx.send(embed=create_embed("Vote", f"{eliminated.mention} a été éliminé."))
            await remove_player(ctx, eliminated)
        else:
            await ctx.send(embed=create_embed("Vote", "Personne n'a été éliminé."))

    state.votes.clear()
    await check_game_end(ctx)

async def remove_player(ctx, player):
    if player in state.players:
        role = state.players[player]
        state.dead_players.add(player)
        del state.players[player]
        await remove_channel_permissions(player)
        await ctx.send(embed=create_embed("Révélation", f"{player.display_name} était {role}."))

async def check_game_end(ctx):
    roles_alive = [role for role in state.players.values()]
    if roles_alive.count('Loup-Garou') == 0:
        await ctx.send(embed=create_embed("Victoire", "Les villageois ont gagné !"))
        await end_game(ctx)
    elif roles_alive.count('Loup-Garou') >= len(roles_alive) / 2:
        await ctx.send(embed=create_embed("Victoire", "Les Loups-Garous ont gagné !"))
        await end_game(ctx)
    else:
        await night_phase(ctx)

async def end_game(ctx):
    state.game_active = False
    await ctx.send(embed=create_embed("Fin", "La partie est terminée."))
