"""Diagnóstico de tumores: API de clasificación benigno/maligno con FastAPI.
Endpoints:
GET / página web con el formulario (app/index.html)
GET /health estado del servicio y versión del modelo
POST /predict recibe 30 medidas del tumor y devuelve la clase y la confianza
GET /docs documentación automática de FastAPI
El modelo se entrena antes con modelo/entrenar.py y se lee de app/modelo.joblib.
"""
import hmac
import os
from pathlib import Path
from typing import Annotated
import joblib
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
# ---------------------------------------------------------------- Modelo
CARPETA = Path(__file__).parent
# Se carga UNA sola vez al iniciar el servidor (no en cada petición: sería lento).
ARTEFACTO = joblib.load(os.getenv("MODELO_PATH", CARPETA / "modelo.joblib"))
# ---------------------------------------------------------------- Seguridad (Hito 4)
# MOSTRAR_DOCS=0 en producción oculta /docs (menos información para un atacante).
MOSTRAR_DOCS = os.getenv("MOSTRAR_DOCS", "1") == "1"
# API_KEY: si se define (variable de entorno en Render, nunca en el código), /predict
# exige la cabecera x-api-key con ese valor. Vacía = API abierta (Hitos 1 a 3).
API_KEY = os.getenv("API_KEY", "")
app = FastAPI(title="Diagnóstico de tumores", version=ARTEFACTO["version"],
              docs_url="/docs" if MOSTRAR_DOCS else None,
              redoc_url=None, openapi_url="/openapi.json" if MOSTRAR_DOCS else None)


def requiere_llave(x_api_key: str = Header(default="")):
    """Dependencia de FastAPI: 401 si falta la llave y 403 si es incorrecta."""
    if not API_KEY:
        return # sin llave configurada: acceso libre
    if not x_api_key:
        raise HTTPException(401, "Falta la cabecera x-api-key")
    if not hmac.compare_digest(x_api_key, API_KEY): # comparación en tiempo constante
        raise HTTPException(403, "Llave inválida")
# ---------------------------------------------------------------- Entrada
class Tumor(BaseModel):
    """30 medidas del tumor, en el mismo orden que load_breast_cancer.
    Cada medida debe cumplir ge=0 (mayor o igual a 0) y le=10000 (menor o igual);
    la lista debe tener exactamente 30 valores. Si no se cumple, FastAPI
    responde 422 sin llegar al modelo.
    """
    medidas: list[Annotated[float, Field(ge=0, le=10000)]] = Field(
        min_length=30, max_length=30)
# ---------------------------------------------------------------- Endpoints
@app.get("/health")
def salud():
    """Lo consultan Docker, Kubernetes y Render para saber si el servicio está vivo."""
    return {"status": "ok", "version": ARTEFACTO["version"],
            "exactitud": ARTEFACTO["exactitud"]}


@app.post("/predict", dependencies=[Depends(requiere_llave)])
def predecir(t: Tumor):
    """Devuelve la clase más probable y su probabilidad (200), o 422 si los datos no
    son válidos."""
    # El modelo espera una lista de filas; aquí hay una sola fila con 30 columnas
    # en el MISMO orden que en el entrenamiento.
    x = [t.medidas]
    probabilidades = ARTEFACTO["modelo"].predict_proba(x)[0]
    i = int(probabilidades.argmax()) # índice de la clase ganadora
    return {"clase": ARTEFACTO["clases"][i],
            "confianza": round(float(probabilidades[i]), 3)}


@app.get("/", response_class=HTMLResponse)
def inicio():
    """Sirve la página web; esta y la API comparten origen, así que no hay CORS."""
    return (CARPETA / "index.html").read_text(encoding="utf-8")