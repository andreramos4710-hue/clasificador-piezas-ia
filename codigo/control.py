
# control.py
# Control del clasificador de colores TCR5000
# KNN + limpieza + caracteristicas + comunicacion serial

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

ORDENES = {
    "Negro": b"A",
    "Rojo": b"B",
    "Blanco": b"C"
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
# 3. CAPTURAR VENTANA
# ==========================================================

def capturar_ventana(ser, n):
    """
    Recibe n muestras numericas desde Arduino.
    Descarta datos invalidos y valores fuera del rango ADC.
    """

    muestras = []

    while len(muestras) < n:

        linea = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if not linea:
            continue

        try:
            valor = float(linea)
        except ValueError:
            continue

        if 0 <= valor <= 1023:
            muestras.append(valor)

    return np.asarray(muestras, dtype=float)


# ==========================================================
# 4. LIMPIAR VENTANA
# ==========================================================

def limpiar(ventana):
    """
    Aplica exactamente el filtro de media movil
    utilizado en limpiar.py.

    Ventana: 5 muestras.
    Centrado: True.
    Minimo de muestras: 1.

    Conserva el nivel absoluto del sensor.
    No resta la linea base.
    No normaliza la señal.
    """

    ventana = np.asarray(ventana, dtype=float)

    if len(ventana) == 0:
        raise ValueError("La ventana esta vacia.")

    serie = pd.Series(ventana)

    limpia = serie.rolling(
        window=5,
        center=True,
        min_periods=1
    ).mean()

    return limpia.to_numpy(dtype=float)


# ==========================================================
# 5. CALCULAR CARACTERISTICAS
# ==========================================================

def calcular_features(x):
    """
    Calcula las mismas caracteristicas que features.py.
    """

    x = np.asarray(x, dtype=float)

    if len(x) < 2:
        raise ValueError(
            "Se necesitan al menos 2 muestras."
        )

    # Caracteristicas temporales
    media = np.mean(x)
    desviacion = np.std(x)
    minimo = np.min(x)
    maximo = np.max(x)
    rango = maximo - minimo
    energia = np.sum(x ** 2)

    duracion = np.sum(
        np.abs(x - media) > UMBRAL
    )

    # Transformada rapida de Fourier
    x_fft = x - media

    espectro = np.abs(
        np.fft.rfft(x_fft)
    )

    frecuencias = np.fft.rfftfreq(
        len(x_fft),
        d=1 / FS
    )

    # Eliminar componente de 0 Hz
    espectro = espectro[1:]
    frecuencias = frecuencias[1:]

    # Caracteristicas espectrales
    energia_espectral = np.sum(
        espectro ** 2
    )

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
# 6. CLASIFICAR UNA VENTANA
# ==========================================================

def clasificar(ventana):
    caracteristicas = calcular_features(ventana)

    # Mantener el orden original del entrenamiento
    faltantes = [
        c for c in columnas
        if c not in caracteristicas
    ]

    if faltantes:
        raise ValueError(
            f"Caracteristicas faltantes: {faltantes}"
        )

    entrada = pd.DataFrame(
        [[caracteristicas[c] for c in columnas]],
        columns=columnas
    )

    entrada_escalada = escalador.transform(entrada)

    prediccion = modelo.predict(
        entrada_escalada
    )[0]

    return str(prediccion).strip().capitalize()


# ==========================================================
# 7. PROGRAMA PRINCIPAL
# ==========================================================

def main():

    ultima_orden = None
    numero_ventana = 0

    try:

        with serial.Serial(
            PUERTO,
            BAUDIOS,
            timeout=3
        ) as arduino:

            # Esperar reinicio de Arduino
            time.sleep(2)
            arduino.reset_input_buffer()

            print("\nSistema de clasificacion iniciado.")
            print("Sensor TCR5000 conectado.")
            print("Esperando piezas...")
            print("Presiona Ctrl+C para detener.\n")

            while True:

                # 1. CAPTURAR
                ventana = capturar_ventana(
                    arduino,
                    N_MUESTRAS
                )

                # 2. LIMPIAR
                ventana_limpia = limpiar(ventana)

                # 3. CLASIFICAR
                inicio = time.perf_counter()

                color = clasificar(ventana_limpia)

                tiempo_ms = (
                    time.perf_counter() - inicio
                ) * 1000

                numero_ventana += 1

                # 4. ENVIAR ORDEN A ARDUINO
                if color not in ORDENES:
                    print("Clase desconocida:", color)
                    continue

                orden = ORDENES[color]

                if orden != ultima_orden:

                    arduino.write(orden)
                    arduino.flush()

                    ultima_orden = orden

                print(
                    f"Ventana {numero_ventana}: "
                    f"{color} | "
                    f"Orden: {orden.decode()} | "
                    f"Tiempo: {tiempo_ms:.2f} ms"
                )

    except serial.SerialException as error:

        print("\nError de comunicacion serial:", error)
        print("Revisa el puerto COM, el cable y Arduino.")

    except KeyboardInterrupt:

        print("\nControl detenido por el usuario.")

    except Exception as error:

        print("\nError durante el control:", error)

    finally:
        print("Programa finalizado.")


if __name__ == "__main__":
    main()
