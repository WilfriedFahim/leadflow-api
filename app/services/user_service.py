# Import des exceptions HTTP pour gérer les erreurs
from fastapi import HTTPException

# Base temporaire (on la passe en paramètre)
from typing import List, Dict


def create_user_service(fake_users_db: List[Dict], email: str) -> Dict:
    """
    Service qui gère la création d'un utilisateur.
    On sépare la logique métier de la route FastAPI.
    """

    # Vérifie si l'émail existe déjà
    for user in fake_users_db:
        if user["email"] == email:
            raise HTTPException(
                status_code=400,
                detail="Email déjà utilisé"
            )

    new_user = {
        "id": len(fake_users_db) + 1,
        "email": email,
    }

    fake_users_db.append(new_user)

    return new_user