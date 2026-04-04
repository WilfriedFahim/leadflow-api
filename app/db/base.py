# Importe la classe de base SQLAlchemy moderne
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Classe de base commune à tous les modèles SQLAlchemy.
    Toutes les tables de la base hériteront de cette classe.
    """
    pass