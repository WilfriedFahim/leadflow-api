# Import de FastAPI pour créer mon API web
from fastapi import FastAPI

# Import du router users
from app.api.users import router as users_router

# Importe la fonction d'initialisation des tables
from app.db.init_db import init_db

# Crée l'application fastAPI'
app = FastAPI(title="LeadFlow API")

# Déclaration d'une route HTTP GET sur l'URL racine "/"
@app.on_event("startup")
def on_startup() -> None:
    """
    Fonction exécutée automatique au démarrage.
    Son rôle ici :
    * Créer les tables SQLAlchemy si elles n'existent pas encore
    """
    init_db()

# Branche le routeur users sur l'application
app.include_router(users_router)

@app.get("/")
def read_root() -> dict[str, str]:
    """
    Route racine simple pour verifier que l'application tourne
    """
    return {"message": "LeadFlow API is running!"}