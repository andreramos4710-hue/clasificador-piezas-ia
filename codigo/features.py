
# limpiar.py
# Limpia las lecturas del sensor sin eliminar el nivel absoluto de cada color.

import os
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# 1. RUTAS DEL PROYECTO
# ==========================================================

# Este archivo está dentro de /codigo.
# Subimos una carpeta para llegar a la raíz del repositorio.
RUTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ruta_entrada_csv = os.path.join(RUTA_RAIZ, "datos", "datos.csv")
ruta_salida_csv = os.path.join(RUTA_RAIZ, "datos", "datos_limpios.csv")
carpeta_figuras = os.path.join(RUTA_RAIZ, "figuras")
ruta_salida_figura = os.path.join(carpeta_figuras, "limpieza.png")

# Crear las carpetas por si todavía no existen
os.makedirs(os.path.join(RUTA_RAIZ, "datos"), exist_ok=True)
os.makedirs(carpeta_figuras, exist_ok=True)

print("Ruta raíz del proyecto:")
print(RUTA_RAIZ)

print("\nLeyendo archivo:")
print(ruta_entrada_csv)

# ==========================================================
# 2. LEER DATOS
# ==========================================================

if not os.path.exists(ruta_entrada_csv):
    raise FileNotFoundError(
        f"\nNo se encontró el archivo:\n{ruta_entrada_csv}\n"
        "Primero ejecuta adquirir.py para generar datos.csv."
    )

datos = pd.read_csv(ruta_entrada_csv)

print("\nColumnas encontradas:")
print(datos.columns.tolist())

# ==========================================================
# 3. COMPROBAR COLUMNAS
# ==========================================================

columnas_necesarias = ["ventana", "t", "valor", "tipo"]

for columna in columnas_necesarias:
    if columna not in datos.columns:
        raise ValueError(
            f'Falta la columna "{columna}" en datos.csv.\n'
            f"Columnas disponibles: {datos.columns.tolist()}"
        )

# Convertir valor a número.
# Si existe algún dato incorrecto, se convierte en NaN.
datos["valor"] = pd.to_numeric(datos["valor"], errors="coerce")

# Eliminar filas donde no exista una lectura válida
datos = datos.dropna(subset=["valor"]).copy()

if datos.empty:
    raise ValueError(
        '\nERROR: La columna "valor" está vacía.\n'
        "Revisa adquirir.py y verifica que Arduino esté enviando "
        "las lecturas del TCR5000."
    )

# ==========================================================
# 4. ELIMINAR VALORES FUERA DEL RANGO DEL ADC
# ==========================================================

datos = datos[
    (datos["valor"] >= 0) &
    (datos["valor"] <= 1023)
].copy()

if datos.empty:
    raise ValueError(
        "\nERROR: No quedaron datos después del filtrado.\n"
        'Revisa los valores de la columna "valor" en datos.csv.'
    )

# ==========================================================
# 5. FILTRO DE MEDIA MÓVIL
# ==========================================================

# Suavizamos pequeñas variaciones/ruido del sensor.
# NO restamos la línea base porque necesitamos conservar
# el nivel absoluto que diferencia Negro, Rojo y Blanco.

datos["valor_filtrado"] = (
    datos.groupby("ventana")["valor"]
    .transform(
        lambda x: x.rolling(
            window=5,
            center=True,
            min_periods=1
        ).mean()
    )
)

# ==========================================================
# 6. CONSERVAR EL NIVEL ABSOLUTO
# ==========================================================

# Esta será la señal utilizada posteriormente en features.py.
# Conservamos el nivel real de reflectancia de cada color.

datos["valor_limpio"] = datos["valor_filtrado"]

# ==========================================================
# 7. GUARDAR DATOS LIMPIOS
# ==========================================================

datos.to_csv(ruta_salida_csv, index=False)

print("\nDatos limpios guardados correctamente en:")
print(ruta_salida_csv)

# ==========================================================
# 8. MOSTRAR CANTIDAD DE VENTANAS POR CLASE
# ==========================================================

print("\nCantidad de ventanas por clase:")

ventanas_por_clase = (
    datos[["ventana", "tipo"]]
    .drop_duplicates()
    ["tipo"]
    .value_counts()
)

print(ventanas_por_clase)

print("\nCantidad total de ventanas:")
print(datos["ventana"].nunique())

# ==========================================================
# 9. MOSTRAR CANTIDAD DE MUESTRAS POR VENTANA
# ==========================================================

print("\nCantidad de muestras por ventana:")

muestras_por_ventana = datos.groupby("ventana").size()

print(muestras_por_ventana)

# Advertencia si alguna ventana no tiene aproximadamente 200 muestras
ventanas_incompletas = muestras_por_ventana[muestras_por_ventana < 200]

if not ventanas_incompletas.empty:
    print("\nADVERTENCIA:")
    print(
        "Hay ventanas con menos de 200 muestras. "
        "Las nuevas capturas deben tener 200 muestras por ventana."
    )

# ==========================================================
# 10. GRAFICAR UNA VENTANA
# ==========================================================

primera_ventana = datos["ventana"].iloc[0]

ejemplo = datos[
    datos["ventana"] == primera_ventana
].copy()

plt.figure(figsize=(10, 5))

plt.plot(
    ejemplo["t"],
    ejemplo["valor"],
    label="Original",
    alpha=0.6
)

plt.plot(
    ejemplo["t"],
    ejemplo["valor_filtrado"],
    label="Filtrada",
    linewidth=2
)

tipo_ejemplo = ejemplo["tipo"].iloc[0]

plt.title(
    f"Ventana {primera_ventana} - {tipo_ejemplo}"
)

plt.xlabel("Muestra")
plt.ylabel("Valor ADC")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    ruta_salida_figura,
    dpi=300
)

plt.close()

print("\nGráfica guardada correctamente en:")
print(ruta_salida_figura)

# ==========================================================
# 11. FINAL
# ==========================================================

print("\nProceso de limpieza terminado correctamente.")
