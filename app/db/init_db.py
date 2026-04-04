# Importe la base commune qui connait les métadonnées SQLAlchemy
from app.db.base import Base

# Importe le moteur de connexion à la base
from app.db.session import engine

# Importe les modèles pour qu'ils soient enregistrés avant create_all
from app import models  # noqa:F401


def init_db():
    """
    Crée toutes les tables connues par SQLAlchemy.

    Pour l'instant, on utilise create_all pour apprendre.
    Plus tard, on utilisera Alembic pour les migrations.
    """
    Base.metadata.create_all(bind=engine)