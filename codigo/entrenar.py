
# entrenar.py - Semana 7
# Clasificador de colores con sensor TCR5000

import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# 1. Rutas del proyecto
RAIZ = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RUTA_CSV = os.path.join(RAIZ, "datos", "features.csv")
RUTA_MODELO = os.path.join(RAIZ, "modelo.pkl")
RUTA_FIGURA = os.path.join(RAIZ, "figuras", "confusion.png")

os.makedirs(os.path.dirname(RUTA_FIGURA), exist_ok=True)

# 2. Leer los datos
if not os.path.exists(RUTA_CSV):
    print("ERROR: No existe datos/features.csv")
    print("Primero ejecuta features.py")
    raise SystemExit

features = pd.read_csv(RUTA_CSV)

if "etiqueta" not in features.columns:
    print("ERROR: No existe la columna etiqueta.")
    raise SystemExit

print("Ventanas disponibles:")
print(features["etiqueta"].value_counts())

# 3. Comprobar las tres clases
clases = ["Blanco", "Rojo", "Negro"]

features["etiqueta"] = (
    features["etiqueta"].astype(str).str.strip().str.capitalize()
)

conteos = features["etiqueta"].value_counts()

if any(conteos.get(c, 0) < 5 for c in clases):
    print("\nDATOS INSUFICIENTES")
    print("Se necesitan al menos 5 ventanas por color")
    print("para intentar esta evaluacion.")
    print("Objetivo del proyecto: 30 ventanas por color.")
    print("El codigo esta preparado para entrenar.")
    raise SystemExit

# 4. Separar X e y
X = features.drop(columns=["ventana", "etiqueta"])
y = features["etiqueta"]

# 5. Dividir entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    stratify=y,
    random_state=42
)

# 6. Estandarizar datos
escalador = StandardScaler()

X_train_esc = escalador.fit_transform(X_train)
X_test_esc = escalador.transform(X_test)

# 7. Entrenar modelo k-NN
modelo = KNeighborsClassifier(n_neighbors=5)
modelo.fit(X_train_esc, y_train)

# 8. Evaluar modelo
y_pred = modelo.predict(X_test_esc)

exactitud = accuracy_score(y_test, y_pred)

print("\nExactitud:", exactitud)

matriz = confusion_matrix(
    y_test, y_pred, labels=clases
)

print("\nMatriz de confusion:")
print(matriz)
print("Orden de clases:", clases)

# 9. Graficar matriz de confusion
disp = ConfusionMatrixDisplay(
    confusion_matrix=matriz,
    display_labels=clases
)

disp.plot(cmap="Blues", values_format="d")
plt.title("Matriz de confusion - TCR5000")
plt.tight_layout()
plt.savefig(RUTA_FIGURA, dpi=300)
plt.close()

print("Grafica guardada en figuras/confusion.png")

# 10. Guardar modelo
joblib.dump(
    {
        "modelo": modelo,
        "escalador": escalador,
        "columnas": list(X.columns)
    },
    RUTA_MODELO
)

print("Modelo guardado en modelo.pkl")
