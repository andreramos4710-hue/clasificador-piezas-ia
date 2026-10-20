# adquirir.py
# Captura ventanas etiquetadas y las guarda en datos/datos.csv

import serial
import time
import csv
import os


# ==========================================================
# 1. CONFIGURACIÓN
# ==========================================================

PUERTO = 'COM3'
BAUDIOS = 9600
N_MUESTRAS = 200


# ==========================================================
# 2. RUTAS DEL PROYECTO
# ==========================================================

# Detecta automáticamente la carpeta raíz del proyecto
# adquirir.py está dentro de la carpeta "codigo"
RUTA_RAIZ = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

CARPETA_DATOS = os.path.join(
    RUTA_RAIZ,
    'datos'
)

ARCHIVO = os.path.join(
    CARPETA_DATOS,
    'datos.csv'
)

# Crear carpeta datos si no existe
os.makedirs(CARPETA_DATOS, exist_ok=True)


# ==========================================================
# 3. PEDIR INFORMACIÓN DE LA CAPTURA
# ==========================================================

etiqueta = input(
    "Etiqueta de esta pieza (Negro/Rojo/Blanco): "
).strip()

n_ventanas = int(
    input("Cuantas ventanas vas a capturar: ")
)


# ==========================================================
# 4. CONECTAR CON ARDUINO
# ==========================================================

print(f"\nConectando con Arduino en {PUERTO}...")

ser = serial.Serial(
    PUERTO,
    BAUDIOS,
    timeout=1
)

time.sleep(2)

print("Arduino conectado correctamente.")


# ==========================================================
# 5. BUSCAR EL NÚMERO DE LA SIGUIENTE VENTANA
# ==========================================================

ventana = 0

if os.path.exists(ARCHIVO) and os.path.getsize(ARCHIVO) > 0:

    with open(
        ARCHIVO,
        'r',
        newline='',
        encoding='utf-8'
    ) as archivo_lectura:

        lector = csv.DictReader(archivo_lectura)

        ventanas = []

        for fila in lector:

            try:
                ventanas.append(
                    int(fila['ventana'])
                )

            except (ValueError, KeyError):
                pass

        if ventanas:
            ventana = max(ventanas) + 1


# ==========================================================
# 6. ABRIR ARCHIVO CSV
# ==========================================================

archivo_nuevo = (
    not os.path.exists(ARCHIVO)
    or os.path.getsize(ARCHIVO) == 0
)

with open(
    ARCHIVO,
    'a',
    newline='',
    encoding='utf-8'
) as archivo:

    escritor = csv.writer(archivo)

    # Crear encabezado
    if archivo_nuevo:

        escritor.writerow([
            'ventana',
            'p',
            'valor',
            'etiqueta'
        ])

        archivo.flush()


    # ======================================================
    # 7. CAPTURAR VENTANAS
    # ======================================================

    for i in range(n_ventanas):

        input(
            f"\nVentana {ventana} ({etiqueta}). "
            "Presiona Enter para comenzar..."
        )

        # Limpiar datos anteriores del puerto serial
        ser.reset_input_buffer()

        p = 0

        print("Capturando...")

        while p < N_MUESTRAS:

            linea = ser.readline().decode(
                'utf-8',
                errors='ignore'
            ).strip()

            # Ignorar líneas vacías
            if linea == '':
                continue

            try:
                valor = float(linea)

            except ValueError:
                continue

            escritor.writerow([
                ventana,
                p,
                valor,
                etiqueta
            ])

            p += 1

        archivo.flush()

        print(
            f"Ventana {ventana}: "
            f"{N_MUESTRAS} muestras guardadas correctamente."
        )

        ventana += 1


# ==========================================================
# 8. CERRAR ARDUINO
# ==========================================================

ser.close()


# ==========================================================
# 9. RESULTADO
# ==========================================================

print("\nCaptura terminada correctamente.")

print(
    "Datos guardados en:"
)

print(ARCHIVO)