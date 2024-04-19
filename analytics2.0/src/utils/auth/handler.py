import time
import jwt

from src.data.config import JWT_ALGORITHM, JWT_SECRET

def token_response(token: str):
    return {
        "access_token": token
    }

def sign_jwt(user_id: int, email: str):
    payload={
            "user_id": user_id,
            "email": email,
            "expires": time.time() + 60*60*24
        }
    token = jwt.encode(
        payload=payload,
        key=JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    return token_response(token)

def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except: return {}