"""Pruebas automáticas de la API (se ejecutan con: pytest -q).
TestClient simula peticiones HTTP sin levantar un servidor. GitHub Actions las ejecuta en
cada push: si una falla, la imagen no se publica.
"""
from fastapi.testclient import TestClient
from app.main import app

cliente = TestClient(app)

# Primer paciente del dataset Breast Cancer (tumor maligno).
MALIGNO = [17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
           1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003,
           0.006193, 25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601,
           0.1189]


def test_health():
    """El servicio responde y reporta la versión del modelo."""
    assert cliente.get("/health").json()["status"] == "ok"


def test_predict_maligno():
    """Un tumor típico maligno se clasifica bien."""
    r = cliente.post("/predict", json={"medidas": MALIGNO})
    assert r.status_code == 200 and r.json()["clase"] == "malignant"


def test_predict_invalido():
    """Una lista incompleta se rechaza con 422 (validación de Pydantic)."""
    r = cliente.post("/predict", json={"medidas": [1, 2, 3]})
    assert r.status_code == 422


def test_calidad_minima():
    """Prueba de calidad: si el modelo baja de 0.95 de exactitud, el CI falla."""
    assert cliente.get("/health").json()["exactitud"] >= 0.95


def test_llave_requerida(monkeypatch):
    """Hito 4: con API_KEY definida, sin cabecera da 401 y con la correcta da 200."""
    import app.main as m
    monkeypatch.setattr(m, "API_KEY", "secreto-de-prueba")
    datos = {"medidas": MALIGNO}
    assert cliente.post("/predict", json=datos).status_code == 401
    r = cliente.post("/predict", json=datos, headers={"x-api-key": "secreto-de-prueba"})
    assert r.status_code == 200