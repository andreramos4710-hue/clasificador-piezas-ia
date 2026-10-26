
# control.py
# Control del clasificador de colores TCR5000
# KNN + escalador guardado + comunicacion serial

import os
import time
import joblib
import serial
import numpy as np
import pandas as pd

# ==========================================================
# 1. CONFIGURACION
# ==========================================================

PUERTO = "COM3"
BAUDIOS = 115200
N_MUESTRAS = 200
FS = 100.0
UMBRAL = 50

# Ordenes enviadas al Arduino
ORDENES = {
    "Negro": "A",
    "Rojo": "B",
    "Blanco": "C"
}

# ==========================================================
# 2. RUTAS Y CARGA DEL MODELO
# ==========================================================

RAIZ = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RUTA_MODELO = os.path.join(RAIZ, "modelo.pkl")

if not os.path.exists(RUTA_MODELO):
    raise FileNotFoundError(
        f"No se encontro el modelo: {RUTA_MODELO}"
    )

paquete = joblib.load(RUTA_MODELO)

modelo = paquete["modelo"]
escalador = paquete["escalador"]
columnas = paquete["columnas"]

print("Modelo KNN cargado correctamente.")
print("Caracteristicas:", len(columnas))
print("Puerto:", PUERTO)

# ==========================================================
# 3. EXTRAER LAS MISMAS CARACTERISTICAS DE features.py
# ==========================================================

def extraer_caracteristicas(x):
    x = np.asarray(x, dtype=float)

    media = np.mean(x)
    desviacion = np.std(x)
    minimo = np.min(x)
    maximo = np.max(x)
    rango = maximo - minimo
    energia = np.sum(x ** 2)

    duracion = np.sum(
        np.abs(x - media) > UMBRAL
    )

    # FFT: quitar el promedio solo para el espectro
    x_fft = x - media

    espectro = np.abs(np.fft.rfft(x_fft))

    frecuencias = np.fft.rfftfreq(
        len(x_fft),
        d=1 / FS
    )

    espectro = espectro[1:]
    frecuencias = frecuencias[1:]

    energia_espectral = np.sum(espectro ** 2)

    if np.sum(espectro) > 1e-12:
        f_dominante = frecuencias[
            np.argmax(espectro)
        ]

        centroide = (
            np.sum(frecuencias * espectro)
            / np.sum(espectro)
        )
    else:
        f_dominante = 0.0
        centroide = 0.0

    banda_baja = np.sum(
        espectro[
            (frecuencias > 0) &
            (frecuencias < 10)
        ] ** 2
    )

    banda_media = np.sum(
        espectro[
            (frecuencias >= 10) &
            (frecuencias < 25)
        ] ** 2
    )

    banda_alta = np.sum(
        espectro[
            (frecuencias >= 25) &
            (frecuencias <= FS / 2)
        ] ** 2
    )

    return {
        "media": media,
        "desv": desviacion,
        "minimo": minimo,
        "maximo": maximo,
        "rango": rango,
        "energia": energia,
        "duracion": duracion,
        "f_dominante": f_dominante,
        "energia_espectral": energia_espectral,
        "centroide": centroide,
        "banda_baja": banda_baja,
        "banda_media": banda_media,
        "banda_alta": banda_alta
    }

# ==========================================================
# 4. CLASIFICAR UNA VENTANA
# ==========================================================

def clasificar(x):
    caracteristicas = extraer_caracteristicas(x)

    # Mantener exactamente las columnas del entrenamiento
    entrada = pd.DataFrame(
        [[caracteristicas[c] for c in columnas]],
        columns=columnas
    )

    entrada_escalada = escalador.transform(entrada)

    prediccion = modelo.predict(entrada_escalada)[0]

    return str(prediccion).strip().capitalize()

# ==========================================================
# 5. LEER ARDUINO Y ENVIAR ORDENES
# ==========================================================

def main():
    ultima_orden = None
    ventana = []
    numero_ventana = 0

    try:
        with serial.Serial(
            PUERTO,
            BAUDIOS,
            timeout=3
        ) as arduino:

            # Esperar reinicio del Arduino
            time.sleep(2)
            arduino.reset_input_buffer()

            print("\nControl iniciado.")
            print("Coloca una pieza frente al sensor.")
            print("Presiona Ctrl+C para terminar.\n")

            while True:
                linea = arduino.readline().decode(
                    "utf-8",
                    errors="ignore"
                ).strip()

                if not linea:
                    continue

                try:
                    lectura = float(linea)
                except ValueError:
                    # Ignorar lineas que no sean lecturas numericas
                    continue

                ventana.append(lectura)

                if len(ventana) >= N_MUESTRAS:
                    inicio = time.perf_counter()

                    color = clasificar(ventana)

                    if color not in ORDENES:
                        print("Clase desconocida:", color)
                        ventana = []
                        continue

                    orden = ORDENES[color]

                    # Solo enviar cuando cambia la clase
                    if orden != ultima_orden:
                        arduino.write(orden.encode("ascii"))
                        arduino.flush()
                        ultima_orden = orden

                    tiempo_ms = (
                        time.perf_counter() - inicio
                    ) * 1000

                    numero_ventana += 1

                    print(
                        f"Ventana {numero_ventana}: "
                        f"{color} | Orden: {orden} | "
                        f"Tiempo: {tiempo_ms:.2f} ms"
                    )

                    ventana = []

    except serial.SerialException as error:
        print("\nError de comunicacion serial:", error)
        print("Verifica el puerto, el cable y que no haya")
        print("otro programa usando el Arduino.")

    except KeyboardInterrupt:
        print("\nControl detenido por el usuario.")

    finally:
        print("Programa finalizado.")

if __name__ == "__main__":
    main()
