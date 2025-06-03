import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from starlette.requests import Request

SECRET_KEY = "votre_clé_ultra_secrète"
security = HTTPBearer()

def generate_token(discord_id, username, avatar_url, isAdmin):
    payload = {
        "discord_id": discord_id,
        "username": username,
        "avatar": avatar_url,
        "isAdmin": isAdmin,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def get_current_user(request: Request, token=Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")
