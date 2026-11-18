
# clustering.py
# Agrupamiento K-Means con 4 clusters
# Clasificador de colores con sensor TCR5000

import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# ==========================================================
# 1. RUTAS DEL PROYECTO
# ==========================================================

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
    carpeta_figuras, "clustering.png"
)

# ==========================================================
# 2. LEER DATASET
# ==========================================================

features = pd.read_csv(ruta_entrada)

print("Datos cargados correctamente")
print("Total de ventanas:", len(features))

# ==========================================================
# 3. SEPARAR CARACTERISTICAS Y ETIQUETAS
# ==========================================================

X = features.drop(
    columns=["ventana", "etiqueta"]
)

y = features["etiqueta"]

ventanas = features["ventana"]

print("Numero de caracteristicas:", X.shape[1])

# ==========================================================
# 4. ESTANDARIZAR DATOS
# ==========================================================

escalador = StandardScaler()

X_esc = escalador.fit_transform(X)

# ==========================================================
# 5. APLICAR K-MEANS CON 4 CLUSTERS
# ==========================================================

kmeans = KMeans(
    n_clusters=4,
    n_init=10,
    random_state=42
)

grupos = kmeans.fit_predict(X_esc)

# ==========================================================
# 6. COMPARAR GRUPOS CON ETIQUETAS REALES
# ==========================================================

tabla = pd.crosstab(
    y,
    grupos,
    rownames=["Color real"],
    colnames=["Grupo K-Means"]
)

print("\nTABLA DE COMPARACION")
print(tabla)

# Guardar tabla
tabla.to_csv(
    os.path.join(
        carpeta_figuras,
        "tabla_kmeans.csv"
    )
)

# ==========================================================
# 7. REDUCIR A DOS DIMENSIONES PARA VISUALIZAR
# ==========================================================

pca = PCA(n_components=2)

componentes = pca.fit_transform(X_esc)

varianza = pca.explained_variance_ratio_

print("\nVarianza explicada para la grafica:")
print("PC1:", varianza[0] * 100, "%")
print("PC2:", varianza[1] * 100, "%")
print("Acumulada:", varianza.sum() * 100, "%")

# ==========================================================
# 8. GRAFICAR AGRUPAMIENTOS
# ==========================================================

colores_grupos = {
    0: "blue",
    1: "orange",
    2: "green",
    3: "purple"
}

plt.figure(figsize=(10, 7))

for grupo in sorted(set(grupos)):

    mascara = grupos == grupo

    plt.scatter(
        componentes[mascara, 0],
        componentes[mascara, 1],
        color=colores_grupos[grupo],
        label=f"Grupo {grupo}",
        alpha=0.75,
        s=55
    )

plt.xlabel(
    f"PC1 ({varianza[0] * 100:.2f}%)"
)

plt.ylabel(
    f"PC2 ({varianza[1] * 100:.2f}%)"
)

plt.title(
    "Agrupamiento K-Means con 4 grupos - Sensor TCR5000"
)

plt.legend(title="Grupos encontrados")
plt.grid(alpha=0.3)
plt.tight_layout()

# ==========================================================
# 9. GUARDAR GRAFICA
# ==========================================================

plt.savefig(
    ruta_salida,
    dpi=300
)

plt.show()

print("\nGrafica guardada en:")
print(ruta_salida)

# ==========================================================
# 10. GUARDAR RESULTADOS POR VENTANA
# ==========================================================

resultado = pd.DataFrame({
    "ventana": ventanas,
    "color_real": y,
    "grupo_kmeans": grupos,
    "PC1": componentes[:, 0],
    "PC2": componentes[:, 1]
})

resultado.to_csv(
    os.path.join(
        carpeta_figuras,
        "resultados_kmeans.csv"
    ),
    index=False
)

print("\nResultados guardados correctamente.")
print("\nProceso K-Means terminado.")
