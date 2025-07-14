from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Servidor de indicadores activo"}

@app.get("/indicadores")
def indicadores():
    try:
        with open("indicadores.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "No hay datos aún"}
