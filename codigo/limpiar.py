# limpiar.py
# Limpia los datos del sensor sin eliminar el nivel absoluto de cada color

import os
import pandas as pd
import matplotlib.pyplot as plt


# ==========================================================
# 1. RUTAS DEL PROYECTO
# ==========================================================

# Detecta automáticamente la carpeta raíz del proyecto
RUTA_RAIZ = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ruta_entrada_csv = os.path.join(
    RUTA_RAIZ,
    'datos',
    'datos.csv'
)

ruta_salida_csv = os.path.join(
    RUTA_RAIZ,
    'datos',
    'datos_limpios.csv'
)

carpeta_figuras = os.path.join(
    RUTA_RAIZ,
    'figuras'
)

ruta_salida_figura = os.path.join(
    carpeta_figuras,
    'limpieza.png'
)

# Crear carpeta figuras si no existe
os.makedirs(carpeta_figuras, exist_ok=True)


# ==========================================================
# 2. LEER LOS DATOS
# ==========================================================

datos = pd.read_csv(ruta_entrada_csv)

print("\nDatos cargados correctamente.")
print("Cantidad de muestras originales:", len(datos))

print("\nPrimeras filas:")
print(datos.head())


# ==========================================================
# 3. COMPROBAR COLUMNAS
# ==========================================================

columnas_necesarias = [
    'ventana',
    'p',
    'valor',
    'etiqueta'
]

for columna in columnas_necesarias:

    if columna not in datos.columns:

        raise ValueError(
            f'ERROR: No existe la columna "{columna}" '
            'en datos.csv'
        )


# ==========================================================
# 4. CONVERTIR VALOR A NÚMERO
# ==========================================================

datos['valor'] = pd.to_numeric(
    datos['valor'],
    errors='coerce'
)

# Eliminar filas donde valor no sea válido
datos = datos.dropna(subset=['valor']).copy()


# ==========================================================
# 5. ELIMINAR VALORES FUERA DEL RANGO DEL ARDUINO
# ==========================================================

datos = datos[
    (datos['valor'] >= 0) &
    (datos['valor'] <= 1023)
].copy()

print(
    "Cantidad de muestras después del filtro de rango:",
    len(datos)
)


# ==========================================================
# 6. FILTRO DE MEDIA MÓVIL
# ==========================================================

# Suaviza pequeñas variaciones de ruido.
# IMPORTANTE:
# No se resta la línea base porque necesitamos conservar
# el nivel absoluto que diferencia Negro, Rojo y Blanco.

datos['valor_filtrado'] = (
    datos
    .groupby('ventana')['valor']
    .transform(
        lambda x: x.rolling(
            window=5,
            center=True,
            min_periods=1
        ).mean()
    )
)


# ==========================================================
# 7. CONSERVAR EL NIVEL ABSOLUTO
# ==========================================================

# Usaremos el valor filtrado como señal limpia.
# NO hacemos corrección de línea base por ventana.

datos['valor_limpio'] = datos['valor_filtrado']


# ==========================================================
# 8. COMPROBAR MUESTRAS POR VENTANA
# ==========================================================

muestras_por_ventana = (
    datos.groupby('ventana')
    .size()
)

print("\nMuestras por ventana:")
print(muestras_por_ventana)

ventanas_incompletas = muestras_por_ventana[
    muestras_por_ventana != 200
]

if len(ventanas_incompletas) > 0:

    print("\nADVERTENCIA:")
    print("Estas ventanas no tienen 200 muestras:")

    print(ventanas_incompletas)

else:

    print(
        "\nTodas las ventanas tienen "
        "200 muestras correctamente."
    )


# ==========================================================
# 9. MOSTRAR PROMEDIO POR COLOR
# ==========================================================

promedios = (
    datos
    .groupby('etiqueta')['valor_limpio']
    .mean()
)

print("\nPromedio del sensor por color:")
print(promedios)


# ==========================================================
# 10. GUARDAR DATOS LIMPIOS
# ==========================================================

datos.to_csv(
    ruta_salida_csv,
    index=False
)

print(
    "\nDatos limpios guardados en:",
    ruta_salida_csv
)


# ==========================================================
# 11. CREAR GRÁFICA
# ==========================================================

plt.figure(figsize=(10, 5))

# Mostrar una ventana de ejemplo
ventana_ejemplo = datos['ventana'].iloc[0]

ejemplo = datos[
    datos['ventana'] == ventana_ejemplo
]

plt.plot(
    ejemplo['p'],
    ejemplo['valor'],
    label='Original',
    alpha=0.6
)

plt.plot(
    ejemplo['p'],
    ejemplo['valor_limpio'],
    label='Filtrada',
    linewidth=2
)

plt.xlabel('Número de muestra')
plt.ylabel('Valor del sensor')
plt.title(
    f'Limpieza de señal - Ventana {ventana_ejemplo}'
)

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    ruta_salida_figura,
    dpi=300
)

plt.close()

print(
    "Gráfica guardada en:",
    ruta_salida_figura
)

print("\nProceso de limpieza terminado correctamente.")