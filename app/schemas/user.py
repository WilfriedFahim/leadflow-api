# Import de BaseModel pour créer des schémas de validation de données
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    """
    Schéma utilisé pour valider les données entrantes
    lors de la création d'un utilisateur
    """

    # Adresse email obligatoire avec validation automatique du format
    email: EmailStr

    # Mot de passe obligatoire
    password: str

class UserRead(BaseModel):
    """
    Schéma utilisé pour renvoyer un utilisateur au client.
    On ne renvoie jamais le mot de passe
    """

    # Identifiant de l'utilisateur
    id: int

    #Adresse email de l'utilisateur
    email:  EmailStr

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    """
    Schéma utilisé pour une mise à jour partielle d'un utilisateur.
    Tous les champs sont optionnels, car avec PATCH,
    on peut envoyer seulement les données à modifier.
    """
    #Email optionnel : il peut être absent de la requête
    email: EmailStr | None = None