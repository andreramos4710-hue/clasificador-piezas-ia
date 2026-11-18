
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
    carpeta_figuras, "pca_3d.png"
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

# 5. APLICAR PCA CON TRES COMPONENTES

pca = PCA(n_components=3)

componentes = pca.fit_transform(X_esc)

varianza = pca.explained_variance_ratio_

print("\nVarianza explicada:")
print("PC1:", varianza[0] * 100, "%")
print("PC2:", varianza[1] * 100, "%")
print("PC3:", varianza[2] * 100, "%")

print(
    "Varianza acumulada de las tres:",
    varianza.sum() * 100,
    "%"
)

# 6. GRAFICA TRIDIMENSIONAL

colores = {
    "negro": "black",
    "rojo": "red",
    "blanco": "royalblue"
}

fig = plt.figure(figsize=(11, 8))

ax = fig.add_subplot(111, projection="3d")

for clase in y.unique():

    mascara = y == clase

    ax.scatter(
        componentes[mascara, 0],
        componentes[mascara, 1],
        componentes[mascara, 2],
        label=clase.capitalize(),
        color=colores.get(clase),
        alpha=0.75,
        s=50
    )

# 7. ETIQUETAR LOS TRES EJES

ax.set_xlabel(
    f"PC1 ({varianza[0] * 100:.2f}%)"
)

ax.set_ylabel(
    f"PC2 ({varianza[1] * 100:.2f}%)"
)

ax.set_zlabel(
    f"PC3 ({varianza[2] * 100:.2f}%)"
)

ax.set_title(
    "PCA 3D - Clasificacion de colores TCR5000"
)

ax.legend(title="Color")

plt.tight_layout()

# 8. GUARDAR GRAFICA

plt.savefig(
    ruta_salida,
    dpi=300
)

plt.show()

print("\nGrafica 3D guardada en:")
print(ruta_salida)

# 9. GUARDAR COORDENADAS PCA POR VENTANA

resultado = pd.DataFrame({
    "ventana": ventanas,
    "etiqueta": y,
    "PC1": componentes[:, 0],
    "PC2": componentes[:, 1],
    "PC3": componentes[:, 2]
})

resultado.to_csv(
    os.path.join(
        carpeta_figuras,
        "coordenadas_pca.csv"
    ),
    index=False
)

print("Coordenadas guardadas correctamente.")
print("\nProceso PCA terminado.")
