# Import du router FastAPI pour organiser les endpoints (routes) liées aux utilisateurs
from fastapi import APIRouter, HTTPException

# Import des schémas Pydantic pour la validation et la réponse
from app.schemas.user import UserCreate, UserRead, UserUpdate

# Import local
from app.services.user_service import (
    create_user_service,
    update_user_email_service,
    get_user_service,
    delete_user_service
)


# Création d'un routeur dédié aux utilisateurs
router = APIRouter(
    prefix="/users", #Préfix commun à toutes les routes de ce fichier
    tags=["Users"], # Nom du groupe visible dans Swagger
)

# Faux stockage temporaire en mémoire pour simuler une base de données
fake_users_db: list[dict[str, int | str]] = []

# Endpoint GET pour récupérer tous les utilisateurs
@router.get("/")
def get_users() -> list[dict[str, int |str]]:
    """
    Endpoint HTTP → délègue la logique au service
    Retourne la liste de tous les utilisateurs simulés
    """
    return fake_users_db

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int)-> dict[str, int | str]:
    """
    Endpoint HTTP → délègue la logique au service
    Retourne un utilisateur spécifique à partir de son identifiant.
    """
    return get_user_service(fake_users_db, user_id)

@router.post("/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate) -> dict[str, int | str]:
    """
    Endpoint HTTP → délègue la logique au service
    """
    return create_user_service(
        fake_users_db=fake_users_db,
        email=str(user.email)
    )


@router.patch("/{user_id", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate) -> dict[str, int | str]:
    """
    Endpoint HTTP → délègue la logique au service
    Met à jour partiellement un utilisateur.
    On vérifie que l'utilisateur envoie au moins un champ à modifier.
    """

    # On vérifie que l'émail est fourni
    if user_update.email is None:
        raise HTTPException(
            status_code=400,
            detail="Aucune données à mettre à jour"
        )

    return update_user_email_service(
        fake_users_db=fake_users_db,
        user_id=user_id,
        new_email=str(user_update.email)
    )

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    """
    Endpoint HTTP → délègue la logique au service
    Supprime un utilisateur par son ID
    """
    delete_user_service(fake_users_db, user_id)