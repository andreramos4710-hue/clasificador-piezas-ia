# limpiar.py - quita ruido y normaliza el dataset
import pandas as pd

datos = pd.read_csv('datos/datos.csv')

# Quitar los valores fuera del rango físico del ADC de Arduino
datos = datos[(datos['valor'] >= 0) & (datos['valor'] <= 1023)].copy()

# Aplicar filtro de media móvil dentro de cada ventana
datos['valor_filtrado'] = (
    datos.groupby('ventana')['valor']
    .transform(lambda x: x.rolling(window=5, center=True).mean())
)

# Rellenar los NaN de las orillas con el valor más cercano
datos['valor_filtrado'] = (
    datos.groupby('ventana')['valor_filtrado']
    .transform(lambda x: x.bfill().ffill())
)

# Guardar el dataset limpio
datos.to_csv('datos/datos_limpios.csv', index=False)

print("Limpieza terminada.")
print("Archivo guardado en: datos/datos_limpios.csv")