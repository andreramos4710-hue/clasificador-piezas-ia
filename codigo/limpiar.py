import os
import pandas as pd
import matplotlib.pyplot as plt

# 1. Definir la ruta raíz del proyecto
RUTA_RAIZ = r'C:\Users\ramos\Downloads\7mo\Inteligencia Artificial\clasificador-piezas-ia'

# Definir rutas completas
ruta_entrada_csv = os.path.join(RUTA_RAIZ, 'datos', 'datos.csv')
ruta_salida_csv = os.path.join(RUTA_RAIZ, 'datos', 'datos_limpios.csv')
carpeta_figuras = os.path.join(RUTA_RAIZ, 'figuras')
ruta_salida_figura = os.path.join(carpeta_figuras, 'limpieza.png')

# 2. Leer datos
datos = pd.read_csv(ruta_entrada_csv)

# 3. Quitar valores fuera del rango del Arduino (0 a 1023)
datos = datos[(datos['valor'] >= 0) & (datos['valor'] <= 1023)].copy()

# 4. Aplicar filtro de media móvil dentro de cada ventana
datos['valor_filtrado'] = datos.groupby('ventana')['valor'].transform(
    lambda x: x.rolling(window=5, center=True, min_periods=1).mean()
)

# 5. Rellenar los NaN de las orillas producidos por el filtro
datos['valor_filtrado'] = datos.groupby('ventana')['valor_filtrado'].transform(
    lambda x: x.bfill().ffill()
)

# 6. Calcular la línea base
base = datos[datos['p'] < 20].groupby('ventana')['valor_filtrado'].mean()
base = base.fillna(datos.groupby('ventana')['valor_filtrado'].mean())

# 7. Restar la línea base a cada ventana
datos['valor_corregido'] = datos['valor_filtrado'] - datos['ventana'].map(base)

# 8. Normalizar Min-Max (evitando la división entre cero)
minimo = datos['valor_corregido'].min()
maximo = datos['valor_corregido'].max()

if maximo != minimo:
    datos['valor_normalizado'] = (
        datos['valor_corregido'] - minimo
    ) / (maximo - minimo)
else:
    datos['valor_normalizado'] = 0.0

# 9. Crear carpeta de figuras si no existe
os.makedirs(carpeta_figuras, exist_ok=True)

# Guardar imagen de ejemplo
ventana = datos['ventana'].iloc[0]
ejemplo = datos[datos['ventana'] == ventana]

plt.figure(figsize=(10, 5))
plt.plot(ejemplo['p'], ejemplo['valor'], label='Antes')
plt.plot(ejemplo['p'], ejemplo['valor_corregido'], label='Después')

plt.xlabel('Tiempo / Muestra (p)')
plt.ylabel('Valor')
plt.title('Comparación antes y después de la limpieza')
plt.legend()
plt.grid()

plt.savefig(ruta_salida_figura)
plt.close()

# 10. Guardar dataset limpio
datos_limpios = datos[
    ['ventana', 'p', 'valor_normalizado', 'tipo']
]

datos_limpios.to_csv(ruta_salida_csv, index=False)

# 11. Mostrar resultados
print('Proceso terminado.')
print(f'Archivo creado: {ruta_salida_csv}')
print(f'Figura creada: {ruta_salida_figura}')