# game.py

import discord
import asyncio
import config
import state
from utils import create_embed, mute_voice_channel, unmute_voice_channel, remove_channel_permissions

# Fonctions principales

async def init_channels(guild):
    """Initialise les salons privés pour chaque rôle."""
    state.log_channel = guild.get_channel(config.log_channel_id)
    state.wolf_channel = guild.get_channel(config.wolf_channel_id)
    state.seer_channel = guild.get_channel(config.seer_channel_id)
    state.witch_channel = guild.get_channel(config.witch_channel_id)
    state.voice_channel = guild.get_channel(config.voice_channel_id)
    state.cupidon_channel = guild.get_channel(config.cupidon_channel_id)
    state.amoureux_channel = guild.get_channel(config.amoureux_channel_id)

    channels = [state.log_channel, state.wolf_channel, state.seer_channel, state.witch_channel, state.cupidon_channel, state.amoureux_channel]
    if not all(channels):
        raise ValueError("Un ou plusieurs IDs de salons sont invalides.")

    for channel in [state.wolf_channel, state.seer_channel, state.witch_channel, state.cupidon_channel, state.amoureux_channel]:
        await channel.set_permissions(guild.default_role, read_messages=False)

    for player, role in state.players.items():
        if role == 'Loup-Garou':
            await state.wolf_channel.set_permissions(player, read_messages=True, send_messages=True, add_reactions=True)
        if role == 'Voyante':
            await state.seer_channel.set_permissions(player, read_messages=True, send_messages=True, add_reactions=True)
        if role == 'Sorcière':
            await state.witch_channel.set_permissions(player, read_messages=True, send_messages=True, add_reactions=True)
        if role == 'Cupidon':
            await state.cupidon_channel.set_permissions(player, read_messages=True, send_messages=True, add_reactions=True)

async def start_game(ctx):
    """Démarre la partie."""
    state.game_active = True
    state.votes.clear()
    state.wolf_votes.clear()
    state.dead_players.clear()
    state.amoureux_pair.clear()
    state.vision_used = False
    state.witch_heal_used = False
    state.witch_kill_used = False
    state.victim_of_wolves = None
    state.victim_of_witch = None
    state.tir_cible = None

    # Distribution des rôles
    random.shuffle(state.join_users)
    roles = [role for role, config in config.ROLES_CONFIG.items() for _ in range(config.ROLES_CONFIG[role]['quantity'])]
    random.shuffle(roles)

    for member, role in zip(state.join_users, roles):
        state.players[member] = role
        try:
            await member.send(f"Vous êtes **{role}** {config.ROLES_CONFIG[role]['emoji']}")
        except:
            pass
        if role == 'Voyante':
            state.voyante = member
        if role == 'Sorcière':
            state.sorciere = member
        if role == 'Cupidon':
            state.cupidon = member
        if role == 'Chasseur':
            state.chasseur = member

    await init_channels(ctx.guild)
    await ctx.send(embed=create_embed("Rôles", "Les rôles ont été attribués."))
    await cupidon_phase(ctx)
    await night_phase(ctx)

async def cupidon_phase(ctx):
    """Phase où Cupidon choisit les amoureux."""
    state.current_phase = 'cupidon'
    if state.cupidon and state.cupidon not in state.dead_players:
        await state.cupidon_channel.send(embed=create_embed(
            "Cupidon", "Choisissez deux joueurs avec `!choisir @joueur1 @joueur2`."
        ))
        await asyncio.sleep(90)
        if len(state.amoureux_pair) < 2:
            await state.cupidon_channel.send(embed=create_embed(
                "Cupidon", "⏰ Temps écoulé, pas de couple choisi."
            ))

async def night_phase(ctx):
    """Phase de nuit principale."""
    state.current_phase = 'night'
    state.wolf_votes.clear()
    state.vision_used = False
    state.victim_of_wolves = None
    state.victim_of_witch = None

    await mute_voice_channel()

    await voyante_phase(ctx)
    await loups_phase(ctx)
    await sorciere_phase(ctx)

    await resolve_night(ctx)

async def voyante_phase(ctx):
    if state.voyante and state.voyante not in state.dead_players:
        await state.seer_channel.send(f"{state.voyante.mention}, utilisez `!voir_role @joueur` pour inspecter.")
        await asyncio.sleep(config.PHASE_TIMEOUTS['role_action'])

async def loups_phase(ctx):
    await state.wolf_channel.send(embed=create_embed(
        "Loups-Garous", "Discutez et choisissez une cible avec `!lg_vote @joueur`."
    ))
    await asyncio.sleep(config.PHASE_TIMEOUTS['role_action'])

async def sorciere_phase(ctx):
    if state.sorciere and state.sorciere not in state.dead_players:
        if state.victim_of_wolves and not state.witch_heal_used:
            await state.witch_channel.send(embed=create_embed(
                "Sorcière", f"{state.sorciere.mention}, {state.victim_of_wolves.display_name} est blessé. `!sauver` pour sauver. `!tuer @joueur` pour empoisonner."
            ))
        else:
            await state.witch_channel.send(embed=create_embed(
                "Sorcière", "Vous pouvez encore utiliser `!tuer @joueur` si vous le souhaitez."
            ))
        await asyncio.sleep(config.PHASE_TIMEOUTS['role_action'])

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
        morts = ", ".join(p.display_name for p in deaths)
        await ctx.send(embed=create_embed("☠️ Victimes", f"Ce matin, {morts} ont été retrouvés morts."))
    else:
        await ctx.send(embed=create_embed("🌞", "La nuit fut calme..."))

    await day_phase(ctx)

async def day_phase(ctx):
    state.current_phase = 'day'
    await ctx.send(embed=create_embed(
        "Vote", "Utilisez `!vote @joueur` pour voter contre un suspect."
    ))
    await asyncio.sleep(config.PHASE_TIMEOUTS['day'])
    await end_day_phase(ctx)

async def end_day_phase(ctx):
    async with state.vote_lock:
        if state.votes:
            vote_counts = {}
            for voter, target in state.votes.items():
                vote_counts[target] = vote_counts.get(target, 0) + 1

            eliminated = max(vote_counts, key=vote_counts.get)
            await ctx.send(embed=create_embed(
                "⚖️ Verdict", f"{eliminated.display_name} a été éliminé par le village."
            ))
            await remove_player(ctx, eliminated)
        else:
            await ctx.send(embed=create_embed("⚖️ Verdict", "Personne n'a été éliminé aujourd'hui."))

        state.votes.clear()
        await check_game_end(ctx)

async def remove_player(ctx, player):
    if player not in state.players:
        return

    role = state.players.pop(player)
    state.dead_players.add(player)

    await remove_channel_permissions(player)
    await ctx.send(embed=create_embed("Révélation", f"{player.display_name} était **{role}**."))

    # Amoureux
    if player in state.amoureux_pair:
        for autre in state.amoureux_pair:
            if autre != player and autre not in state.dead_players:
                await ctx.send(embed=create_embed(
                    "💔 Drame", f"{autre.display_name} ne peut vivre sans son amour et meurt également."
                ))
                await remove_player(ctx, autre)

    # Chasseur
    if role == 'Chasseur':
        await ctx.send(embed=create_embed(
            "🏹 Chasseur", f"{player.display_name}, utilisez `!tirer @joueur` pour venger votre mort !"
        ))
        state.tir_cible = player

async def check_game_end(ctx):
    roles_vivants = [role for role in state.players.values()]
    if roles_vivants.count('Loup-Garou') == 0:
        await ctx.send(embed=create_embed("🏆 Victoire", "Les Villageois ont gagné !"))
        await end_game(ctx)
    elif roles_vivants.count('Loup-Garou') >= len(roles_vivants) / 2:
        await ctx.send(embed=create_embed("🌑 Victoire", "Les Loups-Garous ont gagné !"))
        await end_game(ctx)
    else:
        await night_phase(ctx)

async def end_game(ctx):
    state.game_active = False
    await ctx.send(embed=create_embed("🏁 Fin", "La partie est terminée. Merci d'avoir joué !"))
