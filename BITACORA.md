# Bitácora del proyecto

## Semana 1 - Encuadre y configuración del entorno

### Antes de la clase
Se descarga el programa que vamos a utilizar durante el semestre y se configuro el entorno, se configuro nustros repositorio, la busqueda de cosasa mas eficaz utilizando material adquirido, configurando entornos y todo lo que necesita

 ¿Cuál es la diferencia entre programar la regla y aprender la regla? Programar la regla: se define explícitamente qué hacer en cada caso y Aprender la regla: se entrena con ejemplos y el sistema generaliza. 

- ¿Cuál es tu dominio y cuáles son tus tres tipos de pieza? procesamiento de información y asistencia técnica.
1. Pregunta factual → requiere búsqueda y cita.

2. Problema técnico → requiere diagnóstico y guía paso a paso.

3. Creatividad aplicada → requiere ejemplos, tablas, mapas o brainstorming.

- Describe el bucle de control de tu sistema: Sensor (entrada): el texto del usuario (palabras, contexto, idioma).

Modelo (decisión): clasifica si es factual, técnico o creativo y decide la estrategia.

Actuador (salida):

- Si es factual, entrego respuesta con fuentes.

- Si es técnico, doy pasos concretos y verificables.

- Si es creativo, genero comparaciones, tablas o ideas nuevas.

## Semana  2 la primera selñal del sensor 

### Antes de clase 
 1. Que sensor vas a usar y que tipo de salida tiene: usare el sensor tcrt5000 el cual va a ser para detectar el color de los objectos y es de una salida analogica

 2. Tres líneas de ejemplo tal como se van a ver saliendo de tu Arduino, con valores plausibles para tu caso. 
 - 996
 - 1015
 - 1018

 3. Por qué el Arduino no puede mandar Serial.println("Leyendo...").
 El Arduino manda solo datos, nunca mensajes para humanos.

## Bloque 2: leerlo desde Python, y a qué velocidad
# BITÁCORA

## Lectura del sensor TCR5000

Para esta práctica se utilizó un sensor **TCR5000** mediante su salida analógica (AO), conectada a la entrada **A0 del Arduino**.

### 1. ¿Cuánto tarda la pieza en cruzar frente al sensor?

Se estima que la pieza tarda aproximadamente **0.5 segundos** en cruzar frente al sensor TCR5000.

### 2. ¿Qué `delay()` se necesita para tener al menos 20 muestras del evento?

Se necesitan al menos 20 muestras durante los 0.5 segundos que tarda la pieza en pasar.

Se realiza el cálculo:

**0.5 s ÷ 20 muestras = 0.025 s**

Por lo tanto:

**0.025 s = 25 ms**

El `delay()` máximo sería de **25 ms**.

### 3. ¿Cuántas muestras da eso mientras la pieza pasa?

Con un delay de 20  se obtiene aproximadamente:

**1000 ms ÷ 20 ms = 50 muestras por segundo**

Como la pieza tarda aproximadamente 0.5 segundos:

**0.5 s × 50 muestras/s = 25 muestras**

Por lo tanto, se obtienen aproximadamente **25 muestras mientras la pieza pasa frente al sensor**.

Esto supera las **20 muestras mínimas** solicitadas.

### 4. Ajuste del `delay()` en `sensor.ino`
el delay queda en 20 


### Avance del proyecto

prueba agregar
Este es el procedimiento para hacer push:
- Para hacer push primero edito
- Luego hago git add .
- Luego git commit
- Luego git push

