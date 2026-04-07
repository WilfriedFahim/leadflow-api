from fastapi import APIRouter, Depends                        # Import du router FastAPI pour organiser les endpoints (routes) liées aux utilisateurs
from app.schemas.user import UserCreate, UserRead             # Import des schémas Pydantic pour la validation et la réponse
from app.services.user_service import (                       # Import du service
    create_user_service, get_user_service, get_users_service,
)
from app.models.user import User                              # Mon modèle ORM
from app.db.session import get_db                             # Import de la session DB
from sqlalchemy.orm import Session                            # Import du type Session

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

@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
)-> User:
    """
    Endpoint GET connecté à PostgreSQL
    """
    return get_user_service(db=db, user_id=user_id)

@router.get("/", response_model=list[UserRead])
def get_users(db: Session = Depends(get_db)):
    """
    Retourne la liste de tous les utilisateurs.
    """

    return get_users_service(db=db)