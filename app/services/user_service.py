from fastapi import HTTPException      # Import des exceptions HTTP pour gérer les erreurs
from app.models.user import User       # Import du modèle SQLAlchemy User
from sqlalchemy.orm import Session     # Import de BaseModel pour créer des schémas de validation de données

def create_user_service(
        db: Session,  # On reçoit la session DB
        email: str
) -> User:
    """
    Crée un utilisateur en base PostgreSQL.

    Cette fonction :
    * vérifie que l'émail n'existe pas déjà
    * crée un utilisateur SQLAlchemy
    * l'enregistre en base.
    """

    # Vérifie que l'email n'est pas vide
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email déjà utilisé"
        )

    new_user = User(email=email)  # Création de l'objet utilisateur (Pas un Dict)
    db.add(new_user)              # Ajout en base
    db.commit()                   # Sauvegarde réelle en DB
    db.refresh(new_user)          # Recharge l'objet avec les données DB (ex : id auto)

    return new_user


def get_user_service(db: Session, user_id: int) -> User:
    """
    Récupère un utilisateur depuis PostgreSQL.

    Etapes :
    1. Interroger la DB avec db.query
    2. Filtrer sur l'id
    3. Vérifier si on trouve l'utilisateur
    """

    user = db.query(User).filter(User.id == user_id).first()    # Recherche en base de donnée

    # Si on ne trouve pas l'utilisateur → erreur 404.
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable"
        )

    return user