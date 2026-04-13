from passlib.context import CryptContext        # Permet de hasher les mots de passe

# Permet de créer des tokens JWT
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")       # Configuration du hash

SECRET_KEY = "SUPER_SECRET_KEY"     # Clé secrète (à mettre plus tard dans env)

ALGORITHM = "HS256"                 # Algo JWT

ACCESS_TOKEN_EXPIRE_MINUTES = 30    # Expiration token

def hash_password(password: str) -> str:
    """
    Transforme un mot de passe en hash sécurisé.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifie si un mot de passe correspond au hash.
    """
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict) -> str:
    """
    Génère un token JWT avec expiration
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token