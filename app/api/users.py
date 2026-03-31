# Import du router FastAPI pour organiser les endpoints (routes) liées aux utilisateurs
from fastapi import APIRouter

# Import des schémas Pydantic pour la validation et la réponse
from app.schemas.user import UserCreate, UserRead

# Création d'un routeur dédié aux utilisateurs
router = APIRouter(
    prefix="/users", #Préfix commun à toutes les routes de ce fichier
    tags=["Users"], # Nom du groupe visible dans Swagger
)

# Faux stockage temporaire en mémoire pour simuler une base de données
fake_users_db: list[dict[str, int | str]] = []

# Endpoint GET pour récupérer tous les utilisateurs
@router.get("/")
def get_users() -> list[dict]:
    """
    Retourne une liste d'utilisateurs simulés (mock pour le moment).
    Pour l'instant, les données sont stockées en mémoire.
    Plus tard, on branchera PostgreSQL.
    """
    return fake_users_db

@router.post("/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate) -> dict[str, int | str]:
    """
    Crée un utilisateur en utilisant les données validées par Pydantic.

    Pour l'instant :
    * on simule la création
    * on ne stocke pas le mot de passe
    * on renvoie seulement les données publiques.
    """

    # Création d'un nouvel utilisateur simulé
    new_user = {
        "id": len(fake_users_db) + 1,
        "email": str(user.email),
    }

    # Ajout dans notre faux stockage temporaire
    fake_users_db.append(new_user)

    # Retourne uniquement les données publiques de l'utilisateur
    return new_user