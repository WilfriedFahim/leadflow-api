import os                      # Importe le module os pour lire les variables d'environnement
from dotenv import load_dotenv # Importe load_dotenv pour charger automatiquement le fichier .env
load_dotenv()                  # Charge les variables d'environnement depuis la racine du projet.

class Settings:
    """
    Classe de configuration centralisée du projet.
    Son rôle :
    * lire les variables d'environnement
    * fournir ces valeurs au reste de l'application
    """
    # Lit l'URL de connexion PostgresSQL depuis le fichier .env
    # Si la variable n'existe pas, on utilise une valeur par défaut
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/leadflow_db",
    )


# IMPORTANT : cette ligne doit être en dehors de la classe
settings = Settings() # Crée une instance de configuration réutilisable dans tout le projet
