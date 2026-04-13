# Importe les types SQLAlchemy nécessaires pour définir les colonnes
from sqlalchemy import String, Integer

# Importe les outils modernes de mapping SQLAlchemy 2.0
from sqlalchemy.orm import Mapped, mapped_column

# Import la classe de base commune à tous les modèles
from app.db.base import Base

class User(Base):
    """
    Modèle SQLAlchemy représentant la table 'users'.
    Chaque instance de cette classe correspondra à une ligne en base.
    """

    # Nom réel de la table dans PostgreSQL
    __tablename__ = "users"

    # Clé primaire auto-incrémentée
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    # Email utilisateur
    email: Mapped[str] = mapped_column(
        String(225),
        unique=True,    # unique=True empêche les doublons en base
        nullable=False  # nullable=False rend le champs obligatoire
    )

    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False
    )