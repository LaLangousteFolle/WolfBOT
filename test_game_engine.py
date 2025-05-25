# test_game_engine.py

from core.game_engine import GameManager

# Créer une instance de jeu
game = GameManager()

# Étape 1 : Configuration des rôles
print("[CONFIGURATION ROLES]")
game.configure_roles(
    {
        "Loup-Garou": {"quantity": 1},
        "Villageois": {"quantity": 2},
        "Voyante": {"quantity": 1},
    }
)

# Étape 2 : Ajout des joueurs
print("[JOUEURS QUI REJOIGNENT]")
game.join("1", "Alice")
game.join("2", "Bob")
game.join("3", "Charlie")
game.join("4", "Diana")

# Étape 3 : Lancer la partie
print("[DÉMARRAGE DE LA PARTIE]")
game.start_game()

# Afficher l'état actuel
print("\n[ÉTAT APRÈS START]")
state = game.get_state()
for pid, pdata in state["players"].items():
    print(f"{pdata['name']} => rôle: {pdata['role']}, en vie: {pdata['alive']}")

# Étape 4 : Simuler les votes
print("\n[VOTES EN COURS]")
game.vote("1", "2")  # Alice vote Bob
game.vote("2", "3")  # Bob vote Charlie
game.vote("3", "2")  # Charlie vote Bob
game.vote("4", "2")  # Diana vote Bob

# Étape 5 : Résolution du vote
print("\n[RESOLUTION DES VOTES]")
elimine = game.resolve_votes()
if elimine:
    print(f">>> Joueur éliminé : {state['players'][elimine]['name']}")
else:
    print(">>> Personne n'a été éliminé")

# État final
print("\n[ÉTAT FINAL]")
final_state = game.get_state()
for pid, pdata in final_state["players"].items():
    print(f"{pdata['name']} => rôle: {pdata['role']}, en vie: {pdata['alive']}")

# Logs du jeu
print("\n[LOGS]")
for log in final_state["logs"]:
    print(f"- {log}")
