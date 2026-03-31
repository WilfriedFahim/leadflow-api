# Import de FastAPI pour créer mon API web
from fastapi import FastAPI

# Import du router users
from app.api.users import router as users_router

# création de l'application FASTAPI
# Le paramètre title permet d'afficher un nom propre dans Swagger /docs
app = FastAPI(title="LeadFlow API")

# Inclusion des routes users (utilisateurs)
app.include_router(users_router)

# Déclaration d'une route HTTP GET sur l'URL racine "/"
@app.get("/")
def read_root() -> dict[str, str]:
    """
    Route racine pour vérifier que l'API fonctionne.
    """
    return{"message": "LeadFlow API is running"}