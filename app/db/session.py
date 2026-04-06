
from sqlalchemy import create_engine             # Importe create_engine pour créer la connexion à la base
from sqlalchemy.orm import sessionmaker, Session # Importe Session et sessionmaker pour gérer les sessions SQLAlchemy
from app.core.config import settings             # Importe la configuration centralisée

# Crée le moteur SQLAlchemy à partir de l'URL PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # echo=True permet d'afficher les requêtes SQL dans le terminal
)

# Crée une fabrique de sessions SQLAlchemy
# Chaque requête FastAPI pourra obtenir sa propre session
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=Session
)

def get_db():
    """
    Fournit une session de base de données à FastAPI
    Fonctionnement :
    * ouvre une session
    * la fournit à l'endpoint
    * la ferme proprement ensuite
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()