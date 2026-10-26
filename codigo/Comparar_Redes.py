
# Comparar_Redes.py
# Comparacion de KNN contra redes neuronales MLP
# Proyecto: Clasificador de colores con sensor TCR5000

import os
import time
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay

# ==========================================================
# 1. RUTAS DEL PROYECTO
# ==========================================================

RAIZ = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RUTA_CSV = os.path.join(
    RAIZ, "datos", "features.csv"
)

RUTA_MODELO = os.path.join(
    RAIZ, "modelo.pkl"
)

RUTA_FIGURA = os.path.join(
    RAIZ, "figuras", "comparacion_redes.png"
)

os.makedirs(os.path.dirname(RUTA_FIGURA), exist_ok=True)

# ==========================================================
# 2. CARGAR DATOS
# ==========================================================

if not os.path.exists(RUTA_CSV):
    raise FileNotFoundError(
        f"No se encontro features.csv en: {RUTA_CSV}\n"
        "Ejecuta primero: python codigo/features.py"
    )

features = pd.read_csv(RUTA_CSV)

if "etiqueta" not in features.columns:
    raise ValueError(
        "El archivo features.csv no contiene la columna etiqueta."
    )

features["etiqueta"] = (
    features["etiqueta"]
    .astype(str)
    .str.strip()
    .str.capitalize()
)

clases = ["Blanco", "Rojo", "Negro"]

conteos = features["etiqueta"].value_counts()

print("\nMuestras disponibles por color:")
print(conteos)

if any(conteos.get(c, 0) < 5 for c in clases):
    raise ValueError(
        "Se necesitan al menos 5 ventanas por cada color."
    )

# ==========================================================
# 3. PREPARAR CARACTERISTICAS Y ETIQUETAS
# ==========================================================

columnas_excluir = ["ventana", "etiqueta"]

X = features.drop(
    columns=columnas_excluir,
    errors="ignore"
)

# Convertir las caracteristicas a valores numericos
X = X.apply(pd.to_numeric, errors="coerce")

datos_validos = X.notna().all(axis=1)

X = X.loc[datos_validos].reset_index(drop=True)
y = features.loc[datos_validos, "etiqueta"].reset_index(drop=True)

if any(y.value_counts().get(c, 0) < 5 for c in clases):
    raise ValueError(
        "Despues de limpiar los datos faltan muestras por color."
    )

# ==========================================================
# 4. DIVIDIR DATOS PARA ENTRENAMIENTO Y PRUEBA
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    stratify=y,
    random_state=42
)

# Escalador ajustado unicamente con entrenamiento
escalador = StandardScaler()

X_train_esc = escalador.fit_transform(X_train)
X_test_esc = escalador.transform(X_test)

# ==========================================================
# 5. CARGAR KNN DE LA SEMANA 7 O ENTRENARLO
# ==========================================================

if os.path.exists(RUTA_MODELO):
    paquete = joblib.load(RUTA_MODELO)

    if isinstance(paquete, dict) and "modelo" in paquete:
        modelo_knn = paquete["modelo"]
        print("\nSe encontro el modelo guardado de Semana 7.")
    else:
        modelo_knn = KNeighborsClassifier(n_neighbors=5)
        modelo_knn.fit(X_train_esc, y_train)
        print("\nEl modelo guardado no es un paquete compatible.")
        print("Se entrenara un KNN nuevo para esta comparacion.")
else:
    modelo_knn = KNeighborsClassifier(n_neighbors=5)
    modelo_knn.fit(X_train_esc, y_train)
    print("\nNo se encontro modelo.pkl. Se entrenara un KNN nuevo.")

# Para comparar justamente, entrenamos los modelos en la misma
# particion y con el mismo escalador.
# El KNN guardado se usa si sus columnas coinciden.
if (
    isinstance(paquete, dict)
    and "modelo" in paquete
    and "columnas" in paquete
    and list(paquete["columnas"]) == list(X.columns)
):
    # Se evalua el modelo guardado con su propio escalador.
    escalador_knn = paquete["escalador"]
    X_test_knn = escalador_knn.transform(X_test)
    usar_knn_guardado = True
else:
    # Entrenamiento comparable con la particion actual.
    modelo_knn = KNeighborsClassifier(n_neighbors=5)
    modelo_knn.fit(X_train_esc, y_train)
    X_test_knn = X_test_esc
    usar_knn_guardado = False

# ==========================================================
# 6. DEFINIR MODELOS
# ==========================================================

modelos = {
    "KNN Semana 7": (
        modelo_knn,
        X_test_knn
    ),
    "MLP 10 neuronas": (
        MLPClassifier(
            hidden_layer_sizes=(10,),
            activation="relu",
            solver="adam",
            max_iter=2000,
            random_state=42
        ),
        X_test_esc
    ),
    "MLP 50 neuronas": (
        MLPClassifier(
            hidden_layer_sizes=(50,),
            activation="relu",
            solver="adam",
            max_iter=2000,
            random_state=42
        ),
        X_test_esc
    )
}

# Entrenar las redes neuronales con los datos de entrenamiento.
# El KNN ya esta entrenado o fue cargado.
for nombre, (modelo, _) in modelos.items():
    if nombre.startswith("MLP"):
        print(f"\nEntrenando {nombre}...")
        modelo.fit(X_train_esc, y_train)

# ==========================================================
# 7. EVALUAR EXACTITUD Y TIEMPO DE PREDICCION
# ==========================================================

resultados = []

for nombre, (modelo, X_eval) in modelos.items():
    inicio = time.perf_counter()
    predicciones = modelo.predict(X_eval)
    tiempo_ms = (time.perf_counter() - inicio) * 1000

    exactitud = accuracy_score(y_test, predicciones)

    resultados.append({
        "Modelo": nombre,
        "Exactitud": exactitud,
        "Exactitud (%)": round(exactitud * 100, 2),
        "Tiempo prediccion (ms)": round(tiempo_ms, 3)
    })

    print(f"\n{nombre}")
    print(f"Exactitud: {exactitud * 100:.2f}%")
    print(f"Tiempo de prediccion: {tiempo_ms:.3f} ms")

# ==========================================================
# 8. MOSTRAR Y GUARDAR COMPARACION
# ==========================================================

tabla = pd.DataFrame(resultados)

print("\n========================================")
print("RESULTADOS DE LA COMPARACION")
print("========================================")
print(tabla.to_string(index=False))

# Grafica de exactitud
plt.figure(figsize=(9, 5))

plt.bar(
    tabla["Modelo"],
    tabla["Exactitud (%)"]
)

plt.ylabel("Exactitud (%)")
plt.xlabel("Modelo")
plt.title("Comparacion KNN vs redes neuronales MLP")
plt.ylim(0, 100)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(RUTA_FIGURA, dpi=300)
plt.close()

print("\nGrafica guardada en:")
print(RUTA_FIGURA)

# Guardar resultados en CSV
RUTA_RESULTADOS = os.path.join(
    RAIZ, "datos", "comparacion_redes.csv"
)

tabla.to_csv(RUTA_RESULTADOS, index=False)

print("\nTabla guardada en:")
print(RUTA_RESULTADOS)

print("\nComparacion terminada.")
