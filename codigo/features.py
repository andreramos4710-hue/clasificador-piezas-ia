# features.py - extrae características de cada ventana y genera la gráfica de dispersión

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Definir la ruta raíz del proyecto
RUTA_RAIZ = r'C:\Users\ramos\Downloads\7mo\Inteligencia Artificial\clasificador-piezas-ia'

# Rutas de entrada y salida
ruta_entrada_csv = os.path.join(RUTA_RAIZ, 'datos', 'datos_limpios.csv')
ruta_salida_csv = os.path.join(RUTA_RAIZ, 'datos', 'features.csv')
carpeta_figuras = os.path.join(RUTA_RAIZ, 'figuras')
ruta_salida_figura = os.path.join(carpeta_figuras, 'features.png')

# 2. Cargar el dataset limpio
datos = pd.read_csv(ruta_entrada_csv)

# Convertir los valores del sensor a números
datos['valor_normalizado'] = pd.to_numeric(
    datos['valor_normalizado'],
    errors='coerce'
)

# Umbral para medir la duración del evento
UMBRAL = 0.2

filas = []

# 3. Agrupar por ventana y extraer características
for ventana, g in datos.groupby('ventana'):

    # Eliminar valores vacíos
    x = g['valor_normalizado'].dropna().values

    # Si la ventana no tiene datos, se ignora
    if len(x) == 0:
        continue

    etiqueta = g['tipo'].iloc[0]

    fila = {
        'ventana': ventana,
        'media': x.mean(),
        'desv': x.std(),
        'minimo': x.min(),
        'maximo': x.max(),
        'rango': x.max() - x.min(),
        'energia': np.sum(x**2),
        'duracion': np.sum(np.abs(x) > UMBRAL),
        'etiqueta': etiqueta
    }

    filas.append(fila)

# Crear DataFrame con las características
features = pd.DataFrame(filas)

# 4. Crear las carpetas necesarias
os.makedirs(os.path.dirname(ruta_salida_csv), exist_ok=True)
os.makedirs(carpeta_figuras, exist_ok=True)

# Guardar features.csv
features.to_csv(ruta_salida_csv, index=False)

# 5. Generar el diagrama de dispersión
plt.figure(figsize=(8, 6))

for etiqueta, g in features.groupby('etiqueta'):
    plt.scatter(
        g['rango'],
        g['duracion'],
        label=etiqueta,
        s=60,
        alpha=0.8
    )

plt.xlabel('Rango')
plt.ylabel('Duración')
plt.title('Diagrama de Dispersión: Rango vs Duración')
plt.legend()
plt.grid(True)

plt.savefig(ruta_salida_figura)
plt.close()

# 6. Mostrar resultados en consola
print("Proceso completado correctamente:")
print(f"1. Archivo guardado en: {ruta_salida_csv}")
print(f"2. Figura guardada en: {ruta_salida_figura}\n")

print("Resumen de características:")
print(features.head())

print("\nCantidad de ventanas por clase:")
print(features.groupby('etiqueta').size())