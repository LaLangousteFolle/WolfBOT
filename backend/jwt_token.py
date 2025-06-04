import jwt

SECRET_KEY = "votre_clé_ultra_secrète"

def generate_token(discord_id, username, avatar_url, isAdmin=False):
    payload = {
        "discord_id": discord_id,
        "username": username,
        "avatar": avatar_url,
        "isAdmin": isAdmin,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

Val = generate_token('123456789','Val#1811', 'https://b1157417.smushcdn.com/1157417/wp-content/uploads/fish-discus-swimming-825x550.jpg', True)
Nono = generate_token('165748269','Nono#666', 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Loup_gris_%28Canis_lupus_%29.jpg/250px-Loup_gris_%28Canis_lupus_%29.jpg')
test = generate_token('33333','Test#666', 'https://treecouncil.org.uk/wp-content/uploads/2019/10/Tree_Council_Remarkable_Trees.jpg')

print('token val: ', Val)
print('token nono: ', Nono)
print('token test: ', test)

Val_decoded = jwt.decode(Val, SECRET_KEY, algorithms=["HS256"])
Nono_decoded = jwt.decode(Nono, SECRET_KEY, algorithms=["HS256"])
test_decoded = jwt.decode(test, SECRET_KEY, algorithms=["HS256"])

print('Val decoded: ', Val_decoded)
print('Nono decoded: ', Nono_decoded)
print('test decoded: ', test_decoded)