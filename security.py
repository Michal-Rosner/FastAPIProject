import os
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev-fallback-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    """מגבב סיסמה עם bcrypt ומחזיר מחרוזת לשמירה בטבלה."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """משווה סיסמה בהירה ל-hash שמור. מחזיר True אם תואם."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except ValueError:
        return False


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    """יוצר טוקן JWT חתום ב-HS256 עם תוקף ברירת מחדל של 60 דקות."""
    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta is not None else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "sub": subject,
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """מפענח ומאמת טוקן JWT. מחזיר את ה-payload או None אם לא תקין/פג תוקף."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None