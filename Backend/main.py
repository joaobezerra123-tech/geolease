
from fastapi import FastAPI

app = FastAPI(title="GeoLease API")

@app.get("/")
def inicio():
    return {
        "mensagem": "GeoLease API funcionando!",
        "status": "OK"
    }