import os
import discord
import asyncio
import random
import config
import state
from discord import app_commands
from utils import (
    create_embed,
    mute_voice_channel,
    unmute_voice_channel,
    remove_channel_permissions,
    init_channels,
)

ROLE_LORE = {
    "Loup-Garou": "Tu es une créature nocturne. À la nuit tombée, tu chasses en meute, silencieux et sanguinaire...",
    "Voyante": "La lune éclaire ta boule de cristal. Chaque nuit, tu scrutes les âmes pour découvrir leur vraie nature...",
    "Villageois": "Tu es un simple villageois. Ton flair, ton bon sens et ta voix sont tes seules armes...",
    "Sorcière": "Tu concoctes tes potions dans l’ombre. Deux fioles : une pour guérir, l’autre pour tuer...",
    "Cupidon": "Tu bandes ton arc sous les étoiles. Deux cœurs vont s’unir dans l’amour, ou la tragédie...",
    "Chasseur": "Ton doigt est sur la gâchette. Si tu tombes, tu ne partiras pas seul...",
    "Corbeau": "Tu observes dans l'ombre. Chaque nuit, tu peux marquer un joueur qui subira un malus au vote du jour...",
}

ROLE_EMOJIS = {
    "🐺": "Loup-Garou",
    "🔮": "Voyante",
    "👨‍🌾": "Villageois",
    "🧙‍♀️": "Sorcière",
    "💘": "Cupidon",
    "🏹": "Chasseur",
    "🪶": "Corbeau",
}
INCREASE = "➕"
DECREASE = "➖"
VALIDATE = "✅"
EMOJI_TO_ROLE = {v["emoji"]: role for role, v in config.ROLES_CONFIG.items()}

temp_config = {"message": None, "user": None}


@app_commands.command(
    name="config", description="Configurer les rôles de la partie avant de commencer."
)
async def config_command(interaction: discord.Interaction):
    await start_config(interaction)


async def start_config(interaction):
    temp_config["user"] = interaction.user
    embed = build_config_embed()
    msg = await interaction.channel.send(embed=embed)
    temp_config["message"] = msg

    for emoji in ROLE_EMOJIS:
        await msg.add_reaction(emoji)
    await msg.add_reaction(INCREASE)
    await msg.add_reaction(DECREASE)
    await msg.add_reaction(VALIDATE)

    await interaction.response.send_message(
        "🛠 Configuration en cours...", ephemeral=True
    )


def build_config_embed():
    lines = []
    for role, data in config.ROLES_CONFIG.items():
        emoji = data["emoji"]
        qty = data["quantity"]
        lines.append(f"{emoji} **{role}** : {qty}")
    return create_embed("⚙️ Configuration des rôles", "\n".join(lines))


async def start_game(interaction):
    state.join_users.clear()
    state.join_locked = False
    message = await interaction.channel.send(
        embed=create_embed(
            "📝 Inscriptions",
            "Réagissez avec ✅ pour rejoindre la partie ! Vous avez 60 secondes.",
        )
    )
    state.join_message = message
    await message.add_reaction("✅")

    def check(reaction, user):
        return (
            reaction.message.id == message.id
            and str(reaction.emoji) == "✅"
            and not user.bot
        )

    try:
        while not state.join_locked:
            reaction, user = await interaction.client.wait_for(
                "reaction_add", timeout=60.0, check=check
            )
            if user not in state.join_users:
                state.join_users.append(user)
    except asyncio.TimeoutError:
        pass

    if not state.join_locked:
        state.join_locked = True

    await run_game(interaction)


async def lock_game(interaction):
    if not state.join_locked:
        state.join_locked = True
        await interaction.response.send_message(
            "🔒 Inscriptions verrouillées. La partie démarre !"
        )
        await run_game(interaction)
    else:
        await interaction.response.send_message(
            "Les inscriptions sont déjà verrouillées.", ephemeral=True
        )


async def run_game(interaction):
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

    total_roles = sum(
        role_data["quantity"] for role_data in config.ROLES_CONFIG.values()
    )
    if len(state.join_users) < total_roles:
        await interaction.channel.send(
            embed=create_embed(
                "Erreur",
                f"Pas assez de joueurs pour distribuer tous les rôles ({len(state.join_users)}/{total_roles}).",
            )
        )
        state.game_active = False
        return

    random.shuffle(state.join_users)
    roles = [
        role
        for role, role_data in config.ROLES_CONFIG.items()
        for _ in range(role_data["quantity"])
    ]
    random.shuffle(roles)

    tasks = []
    for member, role in zip(state.join_users, roles):
        state.players[member] = role
        tasks.append(
            member.send(
                f"🎭 Tu es **{role}** {config.ROLES_CONFIG[role]['emoji']}\n\n{ROLE_LORE.get(role, 'Prépare-toi pour la partie...')}"
            )
        )
        if role == "Voyante":
            state.voyante = member
        if role == "Sorcière":
            state.sorciere = member
        if role == "Cupidon":
            state.cupidon = member
        if role == "Chasseur":
            state.chasseur = member
        if role == "Corbeau":
            state.corbeau = member

    results = await asyncio.gather(*tasks, return_exceptions=True)
    for member, result in zip(state.join_users, results):
        if isinstance(result, discord.Forbidden):
            await interaction.channel.send(
                embed=create_embed(
                    "Erreur", f"Impossible d'envoyer un DM à {member.display_name}."
                )
            )
        elif isinstance(result, Exception):
            await interaction.channel.send(
                embed=create_embed(
                    "Erreur",
                    f"Une erreur est survenue avec {member.display_name} : {str(result)}",
                )
            )

    await init_channels(interaction.guild)
    await interaction.channel.send(
        embed=create_embed("🎲 Rôles", "Les rôles ont été attribués. Préparez-vous !")
    )
    await night_phase(interaction)


async def night_phase(ctx):
    state.current_phase = "night"
    await mute_voice_channel()
    await corbeau_phase(ctx)
    await cupidon_phase(ctx)
    await voyante_phase(ctx)
    await loups_phase(ctx)
    await sorciere_phase(ctx)
    await resolve_night(ctx)


async def cupidon_phase(ctx):
    state.current_phase = "cupidon"
    if state.cupidon and state.cupidon not in state.dead_players:
        await state.cupidon_channel.send(
            embed=create_embed(
                "💘 Cupidon",
                "Cupidon s’éveille sous les étoiles. Utilisez `!cupidon @joueur1 @joueur2`.",
            )
        )
        for _ in range(45):
            await asyncio.sleep(2)
            if len(state.amoureux_pair) == 2:
                return
        if len(state.amoureux_pair) < 2:
            await state.cupidon_channel.send(
                embed=create_embed(
                    "Cupidon", "⏰ Temps écoulé, aucun couple n’a été formé."
                )
            )


async def voyante_phase(ctx):
    if state.voyante and state.voyante not in state.dead_players:
        await state.seer_channel.send(
            f"{state.voyante.mention}, utilisez `!voir_role @joueur`."
        )
        for _ in range(config.PHASE_TIMEOUTS["role_action"] // 2):
            await asyncio.sleep(2)
            if state.vision_used:
                break


async def loups_phase(ctx):
    await state.wolf_channel.send(
        embed=create_embed(
            "🐺 Loups-Garous", "Discutez et votez avec `!lg_vote @joueur`."
        )
    )
    for _ in range(config.PHASE_TIMEOUTS["role_action"] // 2):
        await asyncio.sleep(2)
        if len(state.wolf_votes) >= len(
            [p for p in state.players if state.players[p] == "Loup-Garou"]
        ):
            break


async def sorciere_phase(ctx):
    if state.sorciere and state.sorciere not in state.dead_players:
        if state.victim_of_wolves and not state.witch_heal_used:
            await state.witch_channel.send(
                embed=create_embed(
                    "Sorcière",
                    f"{state.sorciere.mention}, {state.victim_of_wolves.display_name} est attaqué. `!sauver` ou `!tuer @joueur`.",
                )
            )
        else:
            await state.witch_channel.send(
                embed=create_embed(
                    "Sorcière", "Vous pouvez encore utiliser `!tuer @joueur`."
                )
            )
        for _ in range(config.PHASE_TIMEOUTS["role_action"] // 2):
            await asyncio.sleep(2)
            if state.witch_heal_used or state.witch_kill_used:
                break


async def corbeau_phase(ctx):
    if state.corbeau and state.corbeau not in state.dead_players:
        await state.log_channel.send(
            embed=create_embed(
                "🪶 Corbeau",
                f"{state.corbeau.mention}, utilisez `/marquer @joueur` pour ajouter un malus de votes.",
            )
        )
        await asyncio.sleep(config.PHASE_TIMEOUTS["role_action"])


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
        noms = ", ".join(p.display_name for p in deaths)
        await ctx.send(
            embed=create_embed(
                "☠️ Victimes", f"{noms} ont été retrouvés morts ce matin."
            )
        )
    else:
        await ctx.send(embed=create_embed("🌞 Matin calme", "La nuit fut paisible."))

    await day_phase(ctx)


async def day_phase(ctx):
    state.current_phase = "day"
    living_players = [p for p in state.players if p not in state.dead_players]
    emojis = list(map(chr, range(0x1F1E6, 0x1F1E6 + len(living_players))))
    vote_map = dict(zip(emojis, living_players))

    desc = "\n".join(
        f"{emoji} : {player.display_name}" for emoji, player in vote_map.items()
    )

    malus_info = (
        "\n\n⚠️ Un joueur a été marqué cette nuit..." if state.corbeau_target else ""
    )
    embed = create_embed(
        "📩 Vote anonyme",
        "Réagissez ci-dessous pour voter anonymement :\n\n" + desc + malus_info,
    )

    vote_msg = await ctx.send(embed=embed)
    for emoji in vote_map:
        await vote_msg.add_reaction(emoji)

    for _ in range(config.PHASE_TIMEOUTS["day"] // 2):
        await asyncio.sleep(2)
        msg = await ctx.channel.fetch_message(vote_msg.id)
        counts = [r.count - 1 for r in msg.reactions if r.emoji in vote_map]
        if sum(counts) >= len(vote_map):
            break

    msg = await ctx.channel.fetch_message(vote_msg.id)
    reaction_counts = {
        vote_map[r.emoji]: r.count - 1 for r in msg.reactions if r.emoji in vote_map
    }

    if state.corbeau_target in reaction_counts:
        reaction_counts[state.corbeau_target] -= 2
        if reaction_counts[state.corbeau_target] < 0:
            reaction_counts[state.corbeau_target] = 0
    state.corbeau_target = None  # reset every day

    if reaction_counts:
        max_votes = max(reaction_counts.values())
        candidates = [p for p, count in reaction_counts.items() if count == max_votes]
        eliminated = random.choice(candidates)
        await ctx.send(
            embed=create_embed("⚖️ Verdict", f"{eliminated.display_name} a été éliminé.")
        )
        await remove_player(ctx, eliminated)
    else:
        await ctx.send(
            embed=create_embed("⚖️ Verdict", "Personne n’a été éliminé aujourd’hui.")
        )

    await check_game_end(ctx)


async def remove_player(ctx, player):
    if player not in state.players:
        return

    role = state.players.pop(player)
    state.dead_players.add(player)

    await remove_channel_permissions(player)
    await ctx.send(
        embed=create_embed("✝️ Révélation", f"{player.display_name} était **{role}**.")
    )

    if player in state.amoureux_pair:
        for autre in state.amoureux_pair:
            if autre != player and autre not in state.dead_players:
                await ctx.send(
                    embed=create_embed(
                        "💔 Amour fatal",
                        f"{autre.display_name} se suicide de chagrin...",
                    )
                )
                await remove_player(ctx, autre)

    if role == "Chasseur":
        await ctx.send(
            embed=create_embed(
                "🌽 Chasseur",
                f"{player.display_name}, utilisez `!tirer @joueur` pour venger votre mort.",
            )
        )
        state.tir_cible = player


async def check_game_end(ctx):
    roles_alive = [role for role in state.players.values()]
    if roles_alive.count("Loup-Garou") == 0:
        await ctx.send(
            embed=create_embed("🏆 Victoire Village", "Les Villageois ont gagné !")
        )
        await end_game(ctx)
    elif roles_alive.count("Loup-Garou") >= len(roles_alive) / 2:
        await ctx.send(
            embed=create_embed("🌑 Victoire Loups", "Les Loups-Garous ont gagné !")
        )
        await end_game(ctx)
    else:
        await night_phase(ctx)


async def end_game(ctx):
    state.game_active = False
    await ctx.send(
        embed=create_embed("🏋️ Fin", "La partie est terminée. Merci d'avoir joué !")
    )
