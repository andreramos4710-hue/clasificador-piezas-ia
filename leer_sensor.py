# leer_sensor.py - lee la señal del sensor y grafica una ventana

import serial
import time
import matplotlib.pyplot as plt

# Puerto serial de Arduino
PUERTO = 'COM3'          # El tuyo puede ser otro: COM4, COM5, COM8...
BAUDIOS = 9600

# Número de muestras
N_MUESTRAS = 200         # Con delay(10) son aproximadamente 2 segundos

# Abrir puerto serial
ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)

# El Arduino se reinicia al abrir el puerto
time.sleep(2)

valores = []

print("Leyendo... pasa la pieza frente al sensor")

# Leer datos hasta obtener 200 muestras
while len(valores) < N_MUESTRAS:

    linea = ser.readline().decode('utf-8').strip()

    try:
        valor = float(linea)
    except ValueError:
        continue          # Si la línea no es un número, la saltamos

    valores.append(valor)

    # Mostrar la señal en vivo
    print(valor)

# Cerrar puerto serial
ser.close()

print(f"Listas {len(valores)} muestras")

# -------------------------------------------------
# GRAFICAR LOS DATOS
# -------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(valores)

plt.xlabel("Muestra")
plt.ylabel("Valor del sensor")
plt.title("Señal del sensor")

plt.grid(True)

# Guardar la gráfica
plt.savefig("../figuras/senal.png", dpi=300, bbox_inches="tight")

# Mostrar la gráfica
plt.show()