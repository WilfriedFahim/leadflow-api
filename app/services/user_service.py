# Import des exceptions HTTP pour gérer les erreurs
from fastapi import HTTPException

# Base temporaire (on la passe en paramètre)
from typing import List, Dict


def create_user_service(fake_users_db: List[Dict], email: str) -> Dict:
    """
    Créait un utilisateur
    * Vérifie les doublons
    * Ajoute l'utilisateur
    """

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email obligatoire"
        )

    # Vérifie si l'émail existe déjà
    for user in fake_users_db:
        if user["email"] == email:
            raise HTTPException(
                status_code=400,
                detail="Email déjà utilisé"
            )

    # Création utilisateur
    new_user = {
        "id": len(fake_users_db) + 1,
        "email": email,
    }

    fake_users_db.append(new_user)

    return new_user


def update_user_email_service(fake_users_db: List[Dict], user_id: int, new_email: str) -> Dict:
    """
    Met à jour l'émail d'un utilisateur.
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


def get_user_service(fake_users_db: List[Dict], user_id: int) -> Dict:
    """
    Récupère un utilisateur par son ID.
    """

    for user in fake_users_db:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="Utilisateur introuvable"
    )

def delete_user_service(fake_users_db: List[Dict], user_id: int) -> None:
    """
    Supprime un utilisateur par son ID.
    """

    for index, user in enumerate(fake_users_db):
        if user["id"] == user_id:
            fake_users_db.pop(index)
            return

    raise HTTPException(
        status_code=404,
        detail="Utilisateur introuvable"
    )
