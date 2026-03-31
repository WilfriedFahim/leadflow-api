# Import de BaseModel pour créer des schémas de validation de données
from pydantic import BaseModel, EmailStr

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
    One ne renvoie jamais le mot de passe
    """

    # Identifiant de l'utilisateur
    id: int

    #Adresse email de l'utilisateur
    email:  EmailStr
