# Import des exceptions HTTP pour gérer les erreurs
from fastapi import HTTPException

# Import de TypeDict pour typer plus précisément la structure d'un utilisateur
from typing import TypedDict

class UserDict(TypedDict):
    """
    Représente la structure d'un utilisateur stocké
    dans notre fausse base de mémoire.

    Pour l'instant, un utilisateur possède :
    * un identifiant entier
    * un émail
    """

    id: int
    email: str

def create_user_service(fake_users_db: list[UserDict], email: str) -> UserDict:
    """
    Créait un utilisateur
    * Vérifie les doublons
    * Ajoute l'utilisateur
    """

    #Vérifie que l'email n'est pas vide
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

    # Construit le nouvel utilisateur
    new_user: UserDict = {
        "id": len(fake_users_db) + 1,
        "email": email,
    }

    #Ajoute l'utilisateur crée
    fake_users_db.append(new_user)

    return new_user


def update_user_email_service(fake_users_db: list[UserDict], user_id: int, new_email: str) -> UserDict:
    """
    Met à jour l'émail d'un utilisateur.
    """

    if not new_email:
        raise HTTPException(
            status_code=400,
            detail="Email obligatoire",
        )

    # On cherche l'utilisateur à modifier
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

            # Mise à jour de l'email de l'utilisateur trouvé
            user["email"] = new_email

            return user

    # Si utilisateur non trouvé
    raise HTTPException(
        status_code=404,
        detail="Utilisateur introuvable"
    )


def get_user_service(fake_users_db: list[UserDict], user_id: int) -> UserDict:
    """
    Retourne un utilisateur à partir de son identifiant.
    Si l'utilisateur n'existe pas, on lève une erreur 404.
    """

    # On parcourt la fausse base pour chercher l'utilisateur demandé
    for user in fake_users_db:
        if user["id"] == user_id:
            return user

    # Si aucun utilisateur trouvé : on renvoie une erreur 404.
    raise HTTPException(
        status_code=404,
        detail="Utilisateur introuvable"
    )

def delete_user_service(fake_users_db: list[UserDict], user_id: int) -> None:
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
