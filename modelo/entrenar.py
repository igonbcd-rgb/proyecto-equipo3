"""Entrena el modelo de diagnóstico de tumores y lo guarda en un archivo.
Regresión logística sobre el dataset Breast Cancer de scikit-learn.
Uso: python modelo/entrenar.py [archivo_salida]
"""
import sys
from datetime import datetime, timezone
import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score, classification_report, recall_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
# ---------------------------------------------------------------- Configuración
# Archivo donde se guarda el modelo; la API lo lee al iniciar.
SALIDA = sys.argv[1] if len(sys.argv) > 1 else "app/modelo.joblib"
SEMILLA = 42 # misma semilla = mismo resultado (reproducible)
# ---------------------------------------------------------------- 1. Datos
# load_breast_cancer trae 569 pacientes con 30 medidas del tumor.
# 0 = maligno, 1 = benigno.
datos = load_breast_cancer()
X, y = datos.data, datos.target
NOMBRES_CLASES = list(datos.target_names)
# 70 % para entrenar y 30 % para evaluar. stratify mantiene la proporción de
# cada clase en ambos conjuntos; el modelo nunca ve los datos de prueba.
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.3, random_state=SEMILLA, stratify=y)
# ---------------------------------------------------------------- 2. Modelo
# Pipeline: primero escala las medidas (media 0, desviación 1) y luego aplica
# regresión logística.
modelo = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
modelo.fit(X_tr, y_tr)
# ---------------------------------------------------------------- 3. Evaluación
predicciones = modelo.predict(X_te)
exactitud = accuracy_score(y_te, predicciones) # proporción de aciertos
# Sensibilidad (recall) de la clase maligna (0): de los tumores malignos reales,
# cuántos detecta el modelo.
sensibilidad = recall_score(y_te, predicciones, pos_label=0)
print(classification_report(y_te, predicciones, target_names=NOMBRES_CLASES))
# ---------------------------------------------------------------- 4. Guardar
# Se guarda un diccionario: el modelo y los datos que la API necesita mostrar.
joblib.dump({
    "modelo": modelo,
    "clases": NOMBRES_CLASES,
    "exactitud": round(float(exactitud), 4),
    "version": datetime.now(timezone.utc).strftime(" %Y %m %d %H %M"), # fecha del modelo
}, SALIDA)
print(f"exactitud={exactitud:.3f} sensibilidad_maligno={sensibilidad:.3f} guardado en {SALIDA}")