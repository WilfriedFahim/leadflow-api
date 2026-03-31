# Import du router FastAPI pour organiser les endpoints (routes) liées aux utilisateurs
from fastapi import APIRouter, HTTPException

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
def get_users() -> list[dict[str, int |str]]:
    """
    Retourne la liste de tous les utilisateurs simulés
    """
    return fake_users_db

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int)-> dict[str, int | str]:
    """
    Retourne un utilisateur spécifique à partir de son identifiant.
    Si aucun utilisateur ne correspond à l'identifiant demandé,
    on renvoie une erreur HTTP 404.
    """

    # Parcours de la fausse base pour chercher l'utilisateur correspondant
    for user in fake_users_db:
        # Vérifie si l'identifiant de l'utilisateur courant correspondant
        if user["id"] == user_id:
            # Retourne l'utilisateur trouvé
            return user

    # Si aucun utilisateur n'a été trouvé, on lève une erreur 404.
    raise HTTPException(status_code=404, detail="Utilisateur introuvable")

@router.post("/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate) -> dict[str, int | str]:
    """
    Crée un utilisateur en utilisant les données validées par Pydantic.

    Pour l'instant :
    * on simule la création
    * on ne stocke pas le mot de passe
    * on renvoie seulement les données publiques.
    """

    # Vérifie si l'émail existe déjà
    for existing_user in fake_users_db:
        if existing_user["email"] == str(user.email):
            raise HTTPException(
                status_code=400,
                detail="Email déjà utilisé"
            )

    # Création d'un nouvel utilisateur simulé
    new_user = {
        "id": len(fake_users_db) + 1,
        "email": str(user.email),
    }

    # Ajout dans notre faux stockage temporaire
    fake_users_db.append(new_user)

    # Retourne uniquement les données publiques de l'utilisateur
    return new_user

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    """
    Supprime un utilisateur par son ID
    """

    for index, user in enumerate(fake_users_db):
        if user["id"] == user_id:
            #Supprime l'utilisateur de la liste
            fake_users_db.pop(index)
            return

    raise HTTPException(status_code=404, detail="Utilisateur introuvable")