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


def update_user_email_service(fake_users_db: List[Dict], user_id: int, new_email: str) -> Dict:
    """
    Met à jour l'émail d'un utilisateur.
    Cette fonction contient uniquement la logique métier :
    * vérification existence user
    * vérification doublon email
    * mise à jour
    """

    # On cherche l'utilisateur
    for user in fake_users_db:
        if user["id"] == user_id:

            # Vérifie doublon email
            for existing_user in fake_users_db:
                if (
                    existing_user["email"] == new_email
                    and existing_user["id"] != user_id
                ):
                    raise HTTPException(
                        status_code=400,
                        detail="Email déjà utilisé"
                    )

            # Mise à jour
            user["email"] = new_email

            return user

    # Si user non trouvé
    raise HTTPException(
        status_code=404,
        detail="Utilisateur introuvable"
    )