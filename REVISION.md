# Retroalimentacion

Esto lo llena tu asesor despues de cada revision de avances (semanas 9, 14 y
17). Lo ves haciendo un `git pull` normal de tu repositorio. No lo edites:
crece con una seccion nueva en cada revision, las anteriores no se borran.

Los niveles son los de la rubrica de `evaluacion/individual`: **Excelente**,
**Bueno**, **Suficiente**, **Insuficiente**.

Evidencias, en este curso, es tu codigo en `codigo/`, tus datos en `datos/`,
tus figuras en `figuras/` y la demo del bucle de control.

---

### Nota rápida (2026-09-14)
El bloque 2 de tu `BITACORA.md` responde con un sistema que clasifica consultas de texto (factual/técnico/creativo), no con tu proyecto de sensores y piezas físicas: parece una respuesta de otro contexto, no relacionada con tu clasificador de color. Hay que retomar las tres preguntas del bloque 2 con tu propio sensor y tus tres tipos de pieza. También quedó un archivo `README.mdm` de más junto al `README.md` correcto.

### Nota rápida (2026-09-21) - s05
Esta nota te va a ahorrar semanas, léela con calma. Tus datos crudos son buenísimos: en `datos.csv` el negro da 518-525, el rojo 729-734 y el blanco 941-950. Los tres colores se separan perfecto por nivel, que es justo lo que quieres. Y tu `limpiar.py` borra esa información: le resta a cada ventana su propia línea base, así que el nivel absoluto (lo único que distingue tus colores) desaparece. Ve tu `datos_limpios.csv`: rojo y blanco quedaron los dos en 0.6428571 exacto, idénticos. De ahí salen las filas de `features.csv` con `desv` y `rango` en 0. La causa de fondo es que tus ventanas traen 3 o 4 muestras, no 200: la línea base se calcula con `p < 20` y se come la ventana completa. Dos correcciones: (1) vuelve a capturar con ventanas de verdad (unas 200 muestras por pasada, 30 pasadas por color), y (2) para un dominio de color no restes línea base por ventana, o conserva también el nivel absoluto como característica. Dos detalles más: tu `features.csv` tiene 3 filas, no las 90 que dice tu bitácora (corrige el dato, no el archivo), y `features.py` y `limpiar.py` tienen `RUTA_RAIZ = r'C:\Users\ramos\...'` escrita a mano, así que no corren en ninguna otra máquina. Usa rutas relativas (`datos/datos.csv`) y abre en VS Code la carpeta del repo.
