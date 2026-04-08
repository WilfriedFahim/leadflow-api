from fastapi import APIRouter, Depends, Query                   # Import du router FastAPI pour organiser les endpoints (routes) liées aux utilisateurs

from app.models import User
from app.schemas.user import UserCreate, UserRead               # Import des schémas Pydantic pour la validation et la réponse
from app.services.user_service import (                         # Import du service
    create_user_service, get_user_service, get_users_service,
)
from app.models.user import User                                # Mon modèle ORM
from app.db.session import get_db                               # Import de la session DB
from sqlalchemy.orm import Session                              # Import du type Session

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