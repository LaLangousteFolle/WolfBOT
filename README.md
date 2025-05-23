# 🐺 Wolfbot — Bot Discord de Loups-Garous

Wolfbot est un bot Discord permettant de jouer au jeu des Loups-Garous de Thiercelieux avec un système de commandes slash, des rôles spéciaux, et une gestion automatisée des phases de jeu.

> ⚠️ **Disclaimer** : Ce projet est en cours de développement, non finalisé, et sujet à de nombreux changements. Il est possible que certaines fonctionnalités ne soient pas encore implémentées ou que le bot ne fonctionne pas correctement sur une autre machine que celle du développeur.

---

## 🚀 Fonctionnalités

- Attribution automatique des rôles aux joueurs
- Commandes slash Discord (slash commands)
- Gestion des phases de jour et de nuit
- Pouvoirs spéciaux : Voyante, Sorcière, Cupidon, Chasseur
- Système de vote (jour et loups-garous)
- Canaux privés pour les différents rôles
- Envois de rôles et descriptions en DM
- Fin automatique de partie selon les conditions de victoire

---

## 🧾 Prérequis

- Python 3.11+
- Un bot Discord avec un token valide
- Accès à l’API Discord avec les intents activés
- Un serveur Discord avec les salons configurés

---

## 🛠 Installation

1. Clonez le repo :

   ```bash
   git clone https://github.com/votre-utilisateur/Wolfbot.git
   cd Wolfbot
   ```

2. Créez et activez un environnement virtuel :

   ```bash
   python -m venv venv
   source venv/bin/activate  # pour bash/zsh
   # ou
   source venv/bin/activate.fish  # pour fish
   ```

3. Installez les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

4. Ajoutez un fichier `.env` avec le contenu suivant :

   ```env
   BOT_TOKEN=your_discord_bot_token
   ```

5. Lancez le bot :

   ```bash
   python main.py
   ```

---

## 📁 Arborescence

```
Wolfbot/
├── main.py              # Point d'entrée du bot
├── keep_alive.py        # Serveur Flask pour Railway
├── requirements.txt     # Dépendances Python
├── .env                 # Token Discord (ne pas versionner)
├── config.py            # IDs des salons et config rôles
├── state.py             # État global de la partie
├── game.py              # Logique principale du jeu
├── utils.py             # Fonctions utilitaires
└── commands/            # Dossier des commandes slash
    ├── general.py       # Commandes /start, /stop, /lock
    ├── vote.py          # Commandes de vote
    └── roles.py         # Pouvoirs spéciaux (voyante, etc.)
```

---

## 🛆 Dépendances principales

- [discord.py 2.5.2](https://discordpy.readthedocs.io/)
- Flask
- python-dotenv

---

## 🧠 Rôles supportés

- 🐺 Loup-Garou
- 🔮 Voyante
- 👨‍🌾 Villageois
- 🧙‍♀️ Sorcière
- 💘 Cupidon
- 🌿 Chasseur

---

## 🧪 TODO / Améliorations possibles

- Système de logs / historiques
- Base de données pour stats
- Interface web pour config
- Traduction multi-langue

---

## 📜 Licence

Projet personnel, libre de l'utiliser et de le forker pour vos propres serveurs de jeu !
