import os, hmac, hashlib, base64, json, time
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

def hash_password(password: str) -> str:
    salt=os.urandom(16)
    digest=hashlib.pbkdf2_hmac("sha256",password.encode(),salt,120000)
    return "pbkdf2_sha256$120000$"+base64.urlsafe_b64encode(salt).decode()+"$"+base64.urlsafe_b64encode(digest).decode()

def verify_password(password: str, password_hash: str) -> bool:
    try:
        _, rounds, salt_b64, digest_b64=password_hash.split("$",3)
        salt=base64.urlsafe_b64decode(salt_b64.encode())
        expected=base64.urlsafe_b64decode(digest_b64.encode())
        actual=hashlib.pbkdf2_hmac("sha256",password.encode(),salt,int(rounds))
        return hmac.compare_digest(actual,expected)
    except Exception:
        return False

def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def _unb64(data: str) -> bytes:
    return base64.urlsafe_b64decode(data+"="*((4-len(data)%4)%4))

def create_access_token(user_id: int, expires_minutes: int = 60*24) -> str:
    payload={"sub":str(user_id),"exp":int(time.time())+expires_minutes*60}
    body=_b64(json.dumps(payload,separators=(",",":")).encode())
    sig=_b64(hmac.new(SECRET_KEY.encode(),body.encode(),hashlib.sha256).digest())
    return body+"."+sig

def decode_access_token(token: str):
    try:
        body,sig=token.split(".",1)
        expected=_b64(hmac.new(SECRET_KEY.encode(),body.encode(),hashlib.sha256).digest())
        if not hmac.compare_digest(sig,expected): return None
        payload=json.loads(_unb64(body))
        if int(payload["exp"])<int(time.time()): return None
        return int(payload["sub"])
    except Exception:
        return None
