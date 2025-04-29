# game.py

import discord
import discord
import asyncio
import config
import random
import state
from utils import create_embed, mute_voice_channel, unmute_voice_channel, remove_channel_permissions

# Lore pour chaque rôle
ROLE_LORE = {
    'Loup-Garou': "Tu es une créature nocturne. À la nuit tombée, tu chasses en meute, silencieux et sanguinaire...",
    'Voyante': "La lune éclaire ta boule de cristal. Chaque nuit, tu scrutes les âmes pour découvrir leur vraie nature...",
    'Villageois': "Tu es un simple villageois. Ton flair, ton bon sens et ta voix sont tes seules armes...",
    'Sorcière': "Tu concoctes tes potions dans l’ombre. Deux fioles : une pour guérir, l’autre pour tuer...",
    'Cupidon': "Tu bandes ton arc sous les étoiles. Deux cœurs vont s’unir dans l’amour, ou la tragédie...",
    'Chasseur': "Ton doigt est sur la gâchette. Si tu tombes, tu ne partiras pas seul..."
}

async def init_channels(guild):
    state.log_channel = guild.get_channel(config.log_channel_id)
    state.wolf_channel = guild.get_channel(config.wolf_channel_id)
    state.seer_channel = guild.get_channel(config.seer_channel_id)
    state.witch_channel = guild.get_channel(config.witch_channel_id)
    state.voice_channel = guild.get_channel(config.voice_channel_id)
    state.cupidon_channel = guild.get_channel(config.cupidon_channel_id)
    state.amoureux_channel = guild.get_channel(config.amoureux_channel_id)

    channels = [state.log_channel, state.wolf_channel, state.seer_channel, state.witch_channel, state.cupidon_channel, state.amoureux_channel]
    if not all(channels):
        raise ValueError("Mauvais IDs de salons.")

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

    total_roles = sum(role_data['quantity'] for role_data in config.ROLES_CONFIG.values())
    if len(state.join_users) < total_roles:
        await ctx.send(embed=create_embed("Erreur", f"Pas assez de joueurs pour distribuer tous les rôles ({len(state.join_users)}/{total_roles})."))
        state.game_active = False
        return

    random.shuffle(state.join_users)
    roles = [role for role, role_data in config.ROLES_CONFIG.items() for _ in range(role_data['quantity'])]
    random.shuffle(roles)

    for member, role in zip(state.join_users, roles):
        state.players[member] = role
        try:
            await member.send(
                f"🎭 Tu es **{role}** {config.ROLES_CONFIG[role]['emoji']}\n\n{ROLE_LORE.get(role, 'Prépare-toi pour la partie...')}"
            )
        except discord.Forbidden:
            await ctx.send(embed=create_embed("Erreur", f"Impossible d'envoyer un DM à {member.display_name}."))

        if role == 'Voyante':
            state.voyante = member
        if role == 'Sorcière':
            state.sorciere = member
        if role == 'Cupidon':
            state.cupidon = member
        if role == 'Chasseur':
            state.chasseur = member

    await init_channels(ctx.guild)
    await ctx.send(embed=create_embed("🎲 Rôles", "Les rôles ont été attribués. Préparez-vous !"))
    await night_phase(ctx)

async def night_phase(ctx):
    state.current_phase = 'night'
    state.wolf_votes.clear()
    state.vision_used = False
    state.victim_of_wolves = None
    state.victim_of_witch = None

    await mute_voice_channel()

    await cupidon_phase(ctx)
    await voyante_phase(ctx)
    await loups_phase(ctx)
    await sorciere_phase(ctx)

    await resolve_night(ctx)

async def cupidon_phase(ctx):
    state.current_phase = 'cupidon'
    if state.cupidon and state.cupidon not in state.dead_players:
        await state.cupidon_channel.send(embed=create_embed(
            "💘 Cupidon", "Cupidon s’éveille sous les étoiles, prêt à unir deux âmes. Utilisez `!cupidon @joueur1 @joueur2`."
        ))
        await asyncio.sleep(90)
        if len(state.amoureux_pair) < 2:
            await state.cupidon_channel.send(embed=create_embed("Cupidon", "⏰ Temps écoulé, aucun couple n’a été formé."))

async def voyante_phase(ctx):
    if state.voyante and state.voyante not in state.dead_players:
        await state.seer_channel.send(f"{state.voyante.mention}, utilisez `!voir_role @joueur` pour inspecter.")
        await asyncio.sleep(config.PHASE_TIMEOUTS['role_action'])

async def loups_phase(ctx):
    await state.wolf_channel.send(embed=create_embed("🐺 Loups-Garous", "Discutez et votez avec `!lg_vote @joueur`."))
    await asyncio.sleep(config.PHASE_TIMEOUTS['role_action'])

async def sorciere_phase(ctx):
    if state.sorciere and state.sorciere not in state.dead_players:
        if state.victim_of_wolves and not state.witch_heal_used:
            await state.witch_channel.send(embed=create_embed("Sorcière", f"{state.sorciere.mention}, {state.victim_of_wolves.display_name} est attaqué. `!sauver` ou `!tuer @joueur`."))
        else:
            await state.witch_channel.send(embed=create_embed("Sorcière", "Vous pouvez encore utiliser `!tuer @joueur`."))
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
        noms = ', '.join(p.display_name for p in deaths)
        await ctx.send(embed=create_embed("☠️ Victimes", f"{noms} ont été retrouvés morts ce matin."))
    else:
        await ctx.send(embed=create_embed("🌞 Matin calme", "La nuit fut paisible."))

    await day_phase(ctx)

async def day_phase(ctx):
    state.current_phase = 'day'

    living_players = [p for p in state.players if p not in state.dead_players]
    emojis = list(map(chr, range(0x1F1E6, 0x1F1E6 + len(living_players))) )  # 🇦 -> 🇿
    vote_map = dict(zip(emojis, living_players))

    desc = "\n".join(f"{emoji} : {player.display_name}" for emoji, player in vote_map.items())
    embed = create_embed("📩 Vote anonyme", "Réagissez ci-dessous pour voter anonymement :\n\n" + desc)

    vote_msg = await ctx.send(embed=embed)
    for emoji in vote_map:
        await vote_msg.add_reaction(emoji)

    await asyncio.sleep(config.PHASE_TIMEOUTS['day'])
    msg = await ctx.channel.fetch_message(vote_msg.id)
    reaction_counts = {vote_map[r.emoji]: r.count - 1 for r in msg.reactions if r.emoji in vote_map}

    if reaction_counts:
        max_votes = max(reaction_counts.values())
        candidates = [p for p, count in reaction_counts.items() if count == max_votes]
        eliminated = random.choice(candidates)
        await ctx.send(embed=create_embed("⚖️ Verdict", f"{eliminated.display_name} a été éliminé."))
        await remove_player(ctx, eliminated)
    else:
        await ctx.send(embed=create_embed("⚖️ Verdict", "Personne n’a été éliminé aujourd’hui."))

    await check_game_end(ctx)

async def remove_player(ctx, player):
    if player not in state.players:
        return

    role = state.players.pop(player)
    state.dead_players.add(player)

    await remove_channel_permissions(player)
    await ctx.send(embed=create_embed("✝️ Révélation", f"{player.display_name} était **{role}**."))

    if player in state.amoureux_pair:
        for autre in state.amoureux_pair:
            if autre != player and autre not in state.dead_players:
                await ctx.send(embed=create_embed("💔 Amour fatal", f"{autre.display_name} se suicide de chagrin..."))
                await remove_player(ctx, autre)

    if role == 'Chasseur':
        await ctx.send(embed=create_embed("🏹 Chasseur", f"{player.display_name}, utilisez `!tirer @joueur` pour venger votre mort."))
        state.tir_cible = player

async def check_game_end(ctx):
    roles_alive = [role for role in state.players.values()]
    if roles_alive.count('Loup-Garou') == 0:
        await ctx.send(embed=create_embed("🏆 Victoire Village", "Les Villageois ont gagné !"))
        await end_game(ctx)
    elif roles_alive.count('Loup-Garou') >= len(roles_alive) / 2:
        await ctx.send(embed=create_embed("🌑 Victoire Loups", "Les Loups-Garous ont gagné !"))
        await end_game(ctx)
    else:
        await night_phase(ctx)

async def end_game(ctx):
    state.game_active = False
    await ctx.send(embed=create_embed("🏁 Fin", "La partie est terminée. Merci d'avoir joué !"))
