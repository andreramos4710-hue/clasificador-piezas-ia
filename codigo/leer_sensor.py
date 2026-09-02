# leer_sensor.py - lee la señal del sensor y grafica una ventana

import serial
import time
import matplotlib.pyplot as plt

PUERTO = 'COM3'          # el tuyo puede ser otro: COM4, COM5...
BAUDIOS = 9600
N_MUESTRAS = 200        # con delay(20) son unos 4 segundos

ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
time.sleep(2)            # el Arduino se reinicia al abrir el puerto

valores = []

print("Leyendo... pasa la pieza frente al sensor TCR5000")

while len(valores) < N_MUESTRAS:
    linea = ser.readline().decode('utf-8').strip()

    try:
        valor = float(linea)
    except ValueError:
        continue          # línea incompleta, la saltamos

    valores.append(valor)
    print(valor)          # para ver la señal en vivo

ser.close()

print(f"Listas {len(valores)} muestras")

# Graficar los valores obtenidos
plt.figure(figsize=(10, 5))

plt.plot(valores)

plt.xlabel("Muestra")
plt.ylabel("Valor analógico del TCR5000")
plt.title("Señal del sensor TCR5000")

plt.grid(True)

# Guardar la figura
plt.savefig("../figuras/senal.png", dpi=300, bbox_inches="tight")

# Mostrar la gráfica
plt.show()