import jwt

SECRET_KEY = "votre_clé_ultra_secrète"

def generate_token(discord_id, username, avatar_url, game_id):
    payload = {
        "discord_id": discord_id,
        "username": username,
        "avatar": avatar_url,
        "game_id": game_id,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

test = generate_token('0000','test#1811', 'https://cdn.pixabay.com/photo/2017/06/13/12/54/profile-2398783_1280.png', 'abc123')

print('token', test)

test_decoded = jwt.decode(test, SECRET_KEY, algorithms=["HS256"])

print('decoded token: ', test_decoded)