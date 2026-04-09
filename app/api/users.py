from fastapi import APIRouter, Depends, Query                   # Import du router FastAPI pour organiser les endpoints (routes) liées aux utilisateurs
from sqlalchemy.orm import Session                              # Import du type Session
from app.schemas.user import UserCreate, UserRead, UserUpdate   # Import des schémas Pydantic pour la validation et la réponse
from app.models.user import User                                # Mon modèle ORM
from app.services.user_service import (                         # Import des services liés à la logique métier
    create_user_service,
    get_user_service,
    get_users_service,
    delete_user_service,
    update_user_service,
)
from app.db.session import get_db                               # Import de la session DB


# Création d'un routeur dédié aux utilisateurs
router = APIRouter(
    prefix="/users", # Préfix commun à toutes les routes de ce fichier
    tags=["Users"],  # Nom du groupe visible dans Swagger
)


@router.post("/", response_model=UserRead, status_code=201)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),   # Injection DB
) -> User:
    """
    Endpoint HTTP → délègue la logique au service
    Retourne la liste de tous les utilisateurs simulés
    """
    return create_user_service(
        db=db,
        email=user.email,
    )

@router.get("/", response_model=list[UserRead])
def get_users(
    # limit = nombre maximum d'éléments à retourner
    # ge=1 signifie que la valeur minimum autorisée est 1
    # le=100 signifie que la valeur maximum autorisée est 100
    limit: int = Query(default=50, ge=1, le=100),

    # offset = nombre d'éléments à ignorer avant de commencer la réponse
    # ge=0 signifie que la valeur minimum autorisée est 0
    offset: int = Query(default=0, ge=0),

    # Injection automatique de la session DB
    db: Session = Depends(get_db),
)-> list[User]:

    return get_users_service(
        db=db,
        limit=limit,
        offset=offset,
    )

@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
)-> User:
    """
    Endpoint GET connecté à PostgreSQL
    """
    return get_user_service(
        db=db,
        user_id=user_id
    )

@router.delete("/{user_id}", status_code=204)
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
) -> None:
    """
    Supprime un utilisateur par son identifiant.

    Si l'utilisateur n'existe pas, le service renvoie une erreur 404.
    Si tout va bien, l'API renvoie 204 No Content.
    """

    delete_user_service(
        db=db,
        user_id=user_id,
    )
@router.patch("/{user_id}", response_model=UserRead)
def update_user(
        user_id: int,
        user: UserUpdate,
        db: Session = Depends(get_db),
):
    """
    Met à jour un utilisateur.

    Exemple :
    PATCH /users/1
    {
        "email" : "new@email.com"
    }
    """

    return update_user_service(
        db=db,
        user_id=user_id,
        email=user.email,
    )