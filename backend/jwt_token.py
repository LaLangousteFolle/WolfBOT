import jwt

SECRET_KEY = "votre_clé_ultra_secrète"

def generate_token(discord_id, username, avatar_url):
    payload = {
        "discord_id": discord_id,
        "username": username,
        "avatar": avatar_url,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

test = generate_token('123456','TEST#018', 'https://www.unapaf.fr/webcontenu/uploads/2018/10/Renard.jpg')

print('token', test)

test_decoded = jwt.decode(test, SECRET_KEY, algorithms=["HS256"])

print('decoded token: ', test_decoded)