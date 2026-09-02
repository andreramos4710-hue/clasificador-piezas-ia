

# adquirir.py - captura ventanas etiquetadas y las guarda en datos/datos.csv

import serial
import time
import csv
import os
import pandas as pd

PUERTO = 'COM3'
BAUDIOS = 9600
N_MUESTRAS = 200
ARCHIVO = 'datos/datos.csv'

etiqueta = input("Etiqueta de esta pieza: ")
n_ventanas = int(input("Cuantas ventanas vas a capturar: "))

# Crear carpeta datos si no existe
os.makedirs('datos', exist_ok=True)

ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)

# 'a' = append: no borra los datos anteriores
archivo = open(ARCHIVO, 'a', newline='')
escritor = csv.writer(archivo)

# TODO 1 RESUELTO:
# Si el archivo está vacío, escribir los encabezados
if os.path.getsize(ARCHIVO) == 0:
    escritor.writerow(['ventana', 't', 'valor', 'etiqueta'])
    archivo.flush()

# TODO 2 RESUELTO:
# Leer el CSV y continuar desde la siguiente ventana
if os.path.getsize(ARCHIVO) > 0:
    datos = pd.read_csv(ARCHIVO)

    if not datos.empty:
        ventana = int(datos['ventana'].max()) + 1
    else:
        ventana = 0
else:
    ventana = 0

for i in range(n_ventanas):

    input(f"\nVentana {ventana} ({etiqueta}). Enter y pasa la pieza...")

    ser.reset_input_buffer()

    t = 0

    while t < N_MUESTRAS:

        linea = ser.readline().decode('utf-8').strip()

        try:
            valor = float(linea)
        except ValueError:
            continue

        escritor.writerow([ventana, t, valor, etiqueta])
        t += 1

    archivo.flush()

    print(f"  {N_MUESTRAS} muestras guardadas")

    ventana += 1

archivo.close()
ser.close()

print(f"\nListo. Datos en {ARCHIVO}")

