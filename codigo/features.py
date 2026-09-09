import pandas as pd
import numpy as np

UMBRAL = 50

datos = pd.read_csv('datos/datos_limpios.csv')

filas = []

for ventana, g in datos.groupby('ventana'):

    # Valores del sensor
    x = g['valor_normalizado'].dropna().values

    # Evitar errores si una ventana no tiene datos
    if len(x) == 0:
        continue

    etiqueta = g['tipo'].iloc[0]

    duracion = np.sum(np.abs(x) > UMBRAL)

    fila = {
        'ventana': ventana,
        'rango': x.max() - x.min(),
        'duracion': duracion,
        'etiqueta': etiqueta
    }

    filas.append(fila)

features = pd.DataFrame(filas)

features.to_csv('datos/features.csv', index=False)

print(features.head())

print("\nCantidad de ventanas por clase:")
print(features.groupby('etiqueta').size())