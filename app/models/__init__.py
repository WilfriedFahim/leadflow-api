# Importe le modèle User pour que SQLAlchemy le connaisse
from app.models.user import User

# Rend l'export explicite
__all__ = ["User"]