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

    new_user = User(email=email)    # Création de l'objet utilisateur (Pas un Dict)
    db.add(new_user)                # Ajout en base
    db.commit()                     # Sauvegarde réelle en DB
    db.refresh(new_user)            # Recharge l'objet avec les données depuis la DB après commit (ex : id auto)

    return new_user


def get_user_service(db: Session, user_id: int) -> User:
    """
    Récupère un utilisateur depuis PostgreSQL à partir de son identifiant.

    Étapes :
    1. Interroger la table users via le modèle User
    2. Filtrer sur l'identifiant
    3. Récupérer le premier résultat
    4. Lever une erreur 404 si aucun utilisateur n'est trouvé
    """

    # Exécute une requête SQLAlchemy :
    # * db.query(User) cible la table users via le modèle User
    # * filter(User.id == user_id) ajoute la condition WHERE id = ...
    # * first() renvoie le premier résultat ou None
    user = db.query(User).filter(User.id == user_id).first()

    # Si aucun utilisateur n'est trouvé, first() renvoie None
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable"
        )

    return user

def get_users_service(db: Session, limit: int =50, offset: int = 0) -> list[User]:
    """
    Récupère une liste paginée d'utilisateur

    Étapes :
    * limit : nombre maximum d'utilisateurs à renvoyer
    * offset : nombre d'utilisateurs à ignorer avant de commencer
    """


    query = db.query(User)          # Construit la requête SQLAlchemy sur la table usersRequête SQLAlchemy
    query = query.offset(offset)    # Applique l'offset pour ignorer les premiers résultats
    query = query.limit(limit)      # Applique la limite pour éviter de tout renvoyer d'un coup
    users = query.all()             # Exécute la requête et renvoie la liste des utilisateurs

    return users
