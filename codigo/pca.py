
# pca.py
# Reduccion de dimensiones mediante PCA
# Clasificador de colores con sensor TCR5000

import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 1. RUTAS DEL PROYECTO

RUTA_RAIZ = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ruta_entrada = os.path.join(
    RUTA_RAIZ, "datos", "features.csv"
)

carpeta_figuras = os.path.join(
    RUTA_RAIZ, "figuras"
)

os.makedirs(carpeta_figuras, exist_ok=True)

ruta_salida = os.path.join(
    carpeta_figuras, "pca.png"
)

# 2. LEER DATASET

features = pd.read_csv(ruta_entrada)

print("Datos cargados correctamente")
print("Total de ventanas:", len(features))

# 3. SEPARAR CARACTERISTICAS Y ETIQUETAS

X = features.drop(
    columns=["ventana", "etiqueta"]
)

y = features["etiqueta"]

ventanas = features["ventana"]

print("Numero de caracteristicas:", X.shape[1])

# 4. ESTANDARIZAR

escalador = StandardScaler()

X_esc = escalador.fit_transform(X)

# 5. APLICAR PCA

pca = PCA(n_components=2)

componentes = pca.fit_transform(X_esc)

varianza = pca.explained_variance_ratio_

print("\nVarianza explicada:")
print("PC1:", varianza[0] * 100, "%")
print("PC2:", varianza[1] * 100, "%")

print(
    "Varianza acumulada:",
    varianza.sum() * 100,
    "%"
)

# 6. GRAFICAR LOS RESULTADOS

colores = {
    "negro": "black",
    "rojo": "red",
    "blanco": "royalblue"
}

plt.figure(figsize=(10, 7))

for clase in y.unique():

    mascara = y == clase

    plt.scatter(
        componentes[mascara, 0],
        componentes[mascara, 1],
        label=clase.capitalize(),
        color=colores.get(clase),
        alpha=0.75
    )

plt.xlabel(
    f"PC1 ({varianza[0] * 100:.2f}%)"
)

plt.ylabel(
    f"PC2 ({varianza[1] * 100:.2f}%)"
)

plt.title(
    "PCA - Clasificacion de colores TCR5000"
)

plt.legend(title="Color")
plt.grid(alpha=0.3)
plt.tight_layout()

# 7. GUARDAR GRAFICA

plt.savefig(
    ruta_salida,
    dpi=300
)

plt.show()

print("\nGrafica guardada en:")
print(ruta_salida)

# 8. GUARDAR COORDENADAS PCA POR VENTANA

resultado = pd.DataFrame({
    "ventana": ventanas,
    "etiqueta": y,
    "PC1": componentes[:, 0],
    "PC2": componentes[:, 1]
})

resultado.to_csv(
    os.path.join(carpeta_figuras, "coordenadas_pca.csv"),
    index=False
)

print("Coordenadas guardadas correctamente.")
print("\nProceso PCA terminado.")
