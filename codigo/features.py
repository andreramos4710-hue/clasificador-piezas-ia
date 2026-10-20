
# features.py
# Extraccion de caracteristicas temporales y espectrales
# Clasificador de colores con sensor TCR5000

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# 1. RUTAS DEL PROYECTO
# ==========================================================

RUTA_RAIZ = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ruta_entrada = os.path.join(
    RUTA_RAIZ, "datos", "datos_limpios.csv"
)

ruta_salida = os.path.join(
    RUTA_RAIZ, "datos", "features.csv"
)

carpeta_figuras = os.path.join(RUTA_RAIZ, "figuras")
os.makedirs(carpeta_figuras, exist_ok=True)

ruta_espectro = os.path.join(
    carpeta_figuras, "espectro.png"
)

ruta_features = os.path.join(
    carpeta_figuras, "features.png"
)

# ==========================================================
# 2. CONFIGURACION
# ==========================================================

FS = 100.0
UMBRAL = 50

colores = {
    "negro": "black",
    "rojo": "red",
    "blanco": "royalblue"
}

# ==========================================================
# 3. LEER DATOS LIMPIOS
# ==========================================================

if not os.path.exists(ruta_entrada):
    raise FileNotFoundError(
        "No se encontro datos_limpios.csv. "
        "Primero ejecuta limpiar.py."
    )

datos = pd.read_csv(ruta_entrada)

# Detectar la columna de clase original
if "etiqueta" in datos.columns:
    columna_clase = "etiqueta"
elif "tipo" in datos.columns:
    columna_clase = "tipo"
else:
    raise ValueError(
        "No existe la columna etiqueta ni tipo."
    )

# Detectar la columna de señal
if "valor_limpio" in datos.columns:
    columna_senal = "valor_limpio"
elif "valor_filtrado" in datos.columns:
    columna_senal = "valor_filtrado"
else:
    raise ValueError(
        "No existe valor_limpio ni valor_filtrado."
    )

if "ventana" not in datos.columns:
    raise ValueError("Falta la columna ventana.")

# Normalizar nombres de colores
datos[columna_clase] = (
    datos[columna_clase]
    .astype(str)
    .str.strip()
    .str.lower()
)

datos[columna_senal] = pd.to_numeric(
    datos[columna_senal],
    errors="coerce"
)

datos = datos.dropna(
    subset=["ventana", columna_senal]
).copy()

datos = datos[
    datos[columna_clase].isin(
        ["negro", "rojo", "blanco"]
    )
].copy()

if datos.empty:
    raise ValueError(
        "No hay muestras validas para procesar."
    )

print("\nDatos cargados correctamente.")
print("Total de muestras:", len(datos))

print("\nMuestras por color:")
print(datos[columna_clase].value_counts())

# ==========================================================
# 4. EXTRAER CARACTERISTICAS POR VENTANA
# ==========================================================

filas = []
espectros_ejemplo = {}

# Agrupar por color y ventana para evitar mezclas
for (etiqueta, ventana), grupo in datos.groupby(
    [columna_clase, "ventana"],
    sort=False
):

    if "t" in grupo.columns:
        grupo = grupo.sort_values("t")
    elif "p" in grupo.columns:
        grupo = grupo.sort_values("p")

    x = grupo[columna_senal].to_numpy(dtype=float)

    if len(x) < 2:
        print("Ventana omitida:", ventana, etiqueta)
        continue

    if len(x) != 200:
        print(
            f"Advertencia: ventana {ventana} "
            f"({etiqueta}) tiene {len(x)} muestras."
        )

    # ------------------------------------------------------
    # 5. CARACTERISTICAS TEMPORALES
    # ------------------------------------------------------

    media = np.mean(x)
    desviacion = np.std(x)
    minimo = np.min(x)
    maximo = np.max(x)
    rango = maximo - minimo
    energia = np.sum(x ** 2)

    duracion = np.sum(
        np.abs(x - media) > UMBRAL
    )

    fila = {
        "ventana": ventana,
        "media": media,
        "desv": desviacion,
        "minimo": minimo,
        "maximo": maximo,
        "rango": rango,
        "energia": energia,
        "duracion": duracion
    }

    # ------------------------------------------------------
    # 6. TRANSFORMADA RAPIDA DE FOURIER (FFT)
    # ------------------------------------------------------

    # Quitar promedio solo para el analisis espectral
    x_fft = x - media

    espectro = np.abs(
        np.fft.rfft(x_fft)
    )

    frecuencias = np.fft.rfftfreq(
        len(x_fft),
        d=1 / FS
    )

    # Eliminar componente de 0 Hz
    espectro = espectro[1:]
    frecuencias = frecuencias[1:]

    # ------------------------------------------------------
    # 7. CARACTERISTICAS ESPECTRALES
    # ------------------------------------------------------

    energia_espectral = np.sum(
        espectro ** 2
    )

    if np.sum(espectro) > 1e-12:

        f_dominante = frecuencias[
            np.argmax(espectro)
        ]

        centroide = (
            np.sum(frecuencias * espectro)
            / np.sum(espectro)
        )

    else:
        f_dominante = 0.0
        centroide = 0.0

    banda_baja = np.sum(
        espectro[
            (frecuencias > 0) &
            (frecuencias < 10)
        ] ** 2
    )

    banda_media = np.sum(
        espectro[
            (frecuencias >= 10) &
            (frecuencias < 25)
        ] ** 2
    )

    banda_alta = np.sum(
        espectro[
            (frecuencias >= 25) &
            (frecuencias <= FS / 2)
        ] ** 2
    )

    fila["f_dominante"] = f_dominante
    fila["energia_espectral"] = energia_espectral
    fila["centroide"] = centroide
    fila["banda_baja"] = banda_baja
    fila["banda_media"] = banda_media
    fila["banda_alta"] = banda_alta

    # GUARDAR LA CLASE COMO ETIQUETA
    fila["etiqueta"] = etiqueta

    filas.append(fila)

    # Guardar primer espectro de cada color
    if etiqueta not in espectros_ejemplo:
        espectros_ejemplo[etiqueta] = (
            frecuencias.copy(),
            espectro.copy()
        )

# ==========================================================
# 8. GUARDAR FEATURES.CSV
# ==========================================================

if not filas:
    raise ValueError(
        "No se pudieron extraer caracteristicas."
    )

features = pd.DataFrame(filas)

features.to_csv(
    ruta_salida,
    index=False
)

print("\nCaracteristicas guardadas en:")
print(ruta_salida)

print("\nVentanas por color:")
print(features["etiqueta"].value_counts())

print("\nTotal de ventanas:", len(features))

# ==========================================================
# 9. GRAFICA FFT POR COLOR
# ==========================================================

plt.figure(figsize=(10, 5))

for clase, (frecuencias, espectro) in (
    espectros_ejemplo.items()
):

    plt.plot(
        frecuencias,
        espectro,
        label=clase.capitalize(),
        color=colores.get(clase, None)
    )

plt.title("Espectro FFT por clase - TCR5000")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Magnitud FFT")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    ruta_espectro,
    dpi=300
)

plt.close()

print("\nGrafica FFT guardada:")
print(ruta_espectro)

# ==========================================================
# 10. GRAFICA DE CARACTERISTICAS POR COLOR
# ==========================================================

plt.figure(figsize=(9, 6))

for clase, grupo in features.groupby("etiqueta"):

    plt.scatter(
        grupo["media"],
        grupo["centroide"],
        label=clase.capitalize(),
        alpha=0.75,
        color=colores.get(clase, None)
    )

plt.xlabel("Media del sensor (ADC)")
plt.ylabel("Centroide espectral (Hz)")
plt.title("Comparacion de caracteristicas por color")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(
    ruta_features,
    dpi=300
)

plt.close()

print("\nGrafica de caracteristicas guardada:")
print(ruta_features)

# ==========================================================
# 11. RESULTADOS FINALES
# ==========================================================

print("\nPromedio de caracteristicas por color:")

columnas = [
    "media",
    "f_dominante",
    "centroide",
    "energia_espectral"
]

print(
    features.groupby("etiqueta")[columnas].mean()
)

print("\nProceso terminado correctamente.")
