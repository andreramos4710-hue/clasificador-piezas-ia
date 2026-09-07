# limpiar.py - quita ruido, corrige linea base y normaliza
import pandas as pd
import matplotlib.pyplot as plt

# Leer datos
datos = pd.read_csv('datos/datos.csv')

# 1. Quitar valores fuera del rango del Arduino
datos = datos[(datos['valor'] >= 0) & (datos['valor'] <= 1023)].copy()

# 2. Aplicar filtro de media movil dentro de cada ventana
datos['valor_filtrado'] = datos.groupby('ventana')['valor'].transform(
    lambda x: x.rolling(window=5, center=True).mean()
)

# 3. Rellenar los NaN de las orillas
datos['valor_filtrado'] = datos.groupby('ventana')['valor_filtrado'].transform(
    lambda x: x.bfill().ffill()
)

# 4. Calcular la linea base usando las primeras 20 muestras
base = datos[datos['t'] < 20].groupby('ventana')['valor_filtrado'].mean()

# 5. Restar la linea base a cada ventana
datos['valor_corregido'] = datos['valor_filtrado'] - datos['ventana'].map(base)

# 6. Normalizar usando Min-Max
minimo = datos['valor_corregido'].min()
maximo = datos['valor_corregido'].max()

datos['valor_normalizado'] = (
    (datos['valor_corregido'] - minimo) /
    (maximo - minimo)
)

# 7. Crear carpeta de figuras si no existe
import os
os.makedirs('figuras', exist_ok=True)

# 8. Graficar una ventana antes y despues de limpiar
ventana = datos['ventana'].iloc[0]
ejemplo = datos[datos['ventana'] == ventana]

plt.figure(figsize=(10, 5))
plt.plot(ejemplo['t'], ejemplo['valor'], label='Antes')
plt.plot(ejemplo['t'], ejemplo['valor_corregido'], label='Después')
plt.xlabel('Tiempo')
plt.ylabel('Valor')
plt.title('Comparación antes y después de la limpieza')
plt.legend()
plt.grid()
plt.savefig('figuras/limpieza.png')
plt.close()

# 9. Guardar dataset limpio
datos_limpios = datos[
    ['ventana', 't', 'valor_normalizado', 'etiqueta']
]

datos_limpios.to_csv('datos/datos_limpios.csv', index=False)

print('Proceso terminado.')
print('Archivo creado: datos/datos_limpios.csv')
print('Figura creada: figuras/limpieza.png')