# Import de FastAPI pour créer mon API web
from fastapi import FastAPI

# création de l'application FASTAPI
# Le paramètre title permet d'afficher un nom propre dans Swagger /docs
app = FastAPI(title="LeadFlow API")

# Déclaration d'une route HTTP GET sur l'URL racine "/"
@app.get("/")
def read_root() -> dict[str, str]:
    """
    Cette fonction est un endpoint de test.
    Elle permet de vérifier rapidement que l'API fonctionne bien
    """
    # Retour d'un dictionnaire Python qui sera converti en JSON par FastAPI
    return{"message": "LeadFlow API is running"}