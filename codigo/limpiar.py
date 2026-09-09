
# limpiar.py - quita ruido, corrige línea base y normaliza

import os
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. Rutas
# ============================================================

CARPETA_PROYECTO = r'C:\Users\ramos\Downloads\7mo\Inteligencia Artificial\clasificador-piezas-ia'

ARCHIVO_ENTRADA = os.path.join(
    CARPETA_PROYECTO,
    'datos',
    'datos.csv'
)

ARCHIVO_SALIDA = os.path.join(
    CARPETA_PROYECTO,
    'datos',
    'datos_limpios.csv'
)

CARPETA_FIGURAS = os.path.join(
    CARPETA_PROYECTO,
    'figuras'
)


# ============================================================
# 2. Leer datos
# ============================================================

datos = pd.read_csv(ARCHIVO_ENTRADA)

print('Columnas encontradas:')
print(datos.columns.tolist())

print()
print('Número de filas originales:', len(datos))


# ============================================================
# 3. Convertir las columnas importantes a número
# ============================================================

datos['valor'] = pd.to_numeric(
    datos['valor'],
    errors='coerce'
)

datos['t'] = pd.to_numeric(
    datos['t'],
    errors='coerce'
)

datos['ventana'] = pd.to_numeric(
    datos['ventana'],
    errors='coerce'
)


# ============================================================
# 4. Eliminar datos vacíos
# ============================================================

datos = datos.dropna(
    subset=['ventana', 't', 'valor']
).copy()

print('Filas después de eliminar vacíos:', len(datos))


# ============================================================
# 5. Quitar valores fuera del rango del Arduino
# ============================================================

datos = datos[
    (datos['valor'] >= 0) &
    (datos['valor'] <= 1023)
].copy()

print('Filas después del filtro 0-1023:', len(datos))


# ============================================================
# 6. Verificar que todavía existan datos
# ============================================================

if datos.empty:
    print()
    print('ERROR: No quedaron datos después del filtrado.')
    print('Revisa los valores de la columna "valor" en datos.csv.')
    exit()


# ============================================================
# 7. Aplicar filtro de media móvil
# ============================================================

datos['valor_filtrado'] = datos.groupby('ventana')['valor'].transform(
    lambda x: x.rolling(
        window=5,
        center=True
    ).mean()
)


# ============================================================
# 8. Rellenar valores vacíos de las orillas
# ============================================================

datos['valor_filtrado'] = datos.groupby('ventana')['valor_filtrado'].transform(
    lambda x: x.bfill().ffill()
)


# ============================================================
# 9. Calcular línea base
#    Primeras 20 muestras de cada ventana
# ============================================================

base = (
    datos[datos['t'] < 20]
    .groupby('ventana')['valor_filtrado']
    .mean()
)


# ============================================================
# 10. Corregir línea base
# ============================================================

datos['valor_corregido'] = (
    datos['valor_filtrado'] -
    datos['ventana'].map(base)
)


# ============================================================
# 11. Normalizar usando Min-Max
# ============================================================

minimo = datos['valor_corregido'].min()
maximo = datos['valor_corregido'].max()

if maximo != minimo:

    datos['valor_normalizado'] = (
        (datos['valor_corregido'] - minimo) /
        (maximo - minimo)
    )

else:

    datos['valor_normalizado'] = 0


# ============================================================
# 12. Crear carpeta de figuras
# ============================================================

os.makedirs(
    CARPETA_FIGURAS,
    exist_ok=True
)


# ============================================================
# 13. Seleccionar una ventana de ejemplo
# ============================================================

ventana = datos['ventana'].iloc[0]

ejemplo = datos[
    datos['ventana'] == ventana
]


# ============================================================
# 14. Graficar antes y después
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(
    ejemplo['t'],
    ejemplo['valor'],
    label='Antes'
)

plt.plot(
    ejemplo['t'],
    ejemplo['valor_corregido'],
    label='Después'
)

plt.xlabel('Muestra (t)')
plt.ylabel('Valor')

plt.title(
    'Comparación antes y después de la limpieza'
)

plt.legend()
plt.grid()

plt.savefig(
    os.path.join(
        CARPETA_FIGURAS,
        'limpieza.png'
    )
)

plt.close()
#

# ============================================================
# 15. Crear dataset limpio
# ============================================================

datos_limpios = datos[
    [
        'ventana',
        't',
        'valor_normalizado',
        'tipo'
    ]
]


# ============================================================
# 16. Guardar dataset
# ============================================================

datos_limpios.to_csv(
    ARCHIVO_SALIDA,
    index=False
)


# ============================================================
# 17. Mensaje final
# ============================================================

print()
print('==========================================')
print('PROCESO TERMINADO CORRECTAMENTE')
print('==========================================')
print('Archivo creado:')
print(ARCHIVO_SALIDA)

print()
print('Figura creada:')
print(
    os.path.join(
        CARPETA_FIGURAS,
        'limpieza.png'
    )
)
