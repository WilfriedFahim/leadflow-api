from pydantic import BaseModel, EmailStr, ConfigDict                # Import de BaseModel pour créer des schémas de validation de données
from typing import Optional

class UserCreate(BaseModel):
    """
    Schéma utilisé pour valider les données entrantes
    lors de la création d'un utilisateur
    """

    email: EmailStr                     # Adresse email obligatoire avec validation automatique du format
    password: str                       # Mot de passe obligatoire

class UserRead(BaseModel):
    """
    Schéma utilisé pour renvoyer un utilisateur au client.
    On ne renvoie jamais le mot de passe
    """

    id: int                             # Identifiant de l'utilisateur
    email:  EmailStr                    # Adresse email de l'utilisateur

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    """
    Schéma utilisé pour une mise à jour partielle d'un utilisateur.
    Tous les champs sont optionnels, car avec PATCH,
    on peut envoyer seulement les données à modifier.
    """

    email: Optional[EmailStr | None] = None       # Email optionnel : il peut être absent de la requête