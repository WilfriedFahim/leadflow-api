from fastapi import HTTPException      # Import des exceptions HTTP pour gérer les erreurs
from app.models.user import User       # Import du modèle SQLAlchemy User
from sqlalchemy.orm import Session     # Import de BaseModel pour créer des schémas de validation de données
from app.core.security import hash_password, verify_password, create_access_token

def create_user_service(db: Session, email: str, password: str) -> User: # On reçoit la session DB
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

    hashed_password = hash_password(password)

    new_user = User(email=email, password_hash=hashed_password)    # Création de l'objet utilisateur (Pas un Dict)

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

def delete_user_service(db: Session, user_id: int) -> None:
    """
    Supprime un utilisateur en base PostgreSQL à partir de son identifiant.

    Étapes :
    1. Chercher l'utilisateur
    2. Lever une erreur 404 s'il n'existe pas
    3. Le supprimer de la session
    4. Commit pour rendre la suppression effective en base de donnée
    """

    # On cherche l'utilisateur à supprimer
    user = db.query(User).filter(User.id == user_id).first()

    # Si aucun utilisateur n'est trouvé, on renvoie une erreur 404.
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable",
        )

    # Marque l'utilisateur pour suppression dans la session SQLAlchemy
    db.delete(user)

    # Valide la suppression en base
    db.commit()

def update_user_service(db: Session, user_id: int, email: str | None ) -> User:
    """
    Met à jour l'émail utilisateur.
    On accepte un email optionnel.

    Etapes :
    1. Vérifier que l'utilisateur existe
    2. Vérifier que le nouvel email n'est pas déjà utilisé
    3. Modifier l'utilisateur
    4. Commit + refresh
    """

    # Vérifie que l'utilisateur existe
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur introuvable",
        )
    if email is not None:

        # Vérifie que l'émail n'est pas déjà utilisé par un autre user
        existing_user = db.query(User).filter(User.email == email).first()

        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=400,
                detail="Email déjà utilisé",
            )
        user.email = email  # Mise à jour

    db.commit()         # Persistance de la db
    db.refresh(user)    # Recharger l'objet apres la persistance

    return user

def login_user_service(db: Session, email: str, password: str) -> str:

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": str(user.id)})

    return token
