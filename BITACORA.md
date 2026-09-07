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

### Avance del proyecto

prueba agregar
Este es el procedimiento para hacer push:
- Para hacer push primero edito
- Luego hago git add .
- Luego git commit
- Luego git push

## Semana  2 la primera selñal del sensor 
## Bloque 1
### Antes de clase 
 1. Que sensor vas a usar y que tipo de salida tiene: usare el sensor tcrt5000 el cual va a ser para detectar el color de los objectos y es de una salida analogica

 2. Tres líneas de ejemplo tal como se van a ver saliendo de tu Arduino, con valores plausibles para tu caso. 
 - 996
 - 1015
 - 1018

 3. Por qué el Arduino no puede mandar Serial.println("Leyendo...").
 El Arduino manda solo datos, nunca mensajes para humanos.

## Bloque 2: leerlo desde Python, y a qué velocidad
## Lectura del sensor TCR5000

Para esta práctica se utilizó un sensor TCR5000 mediante su salida analógica (AO), conectada a la entrada A0 del Arduino.

### ¿Cuánto tarda la pieza en cruzar frente al sensor?

Se estima que la pieza tarda aproximadamente 0.5 segundos en cruzar frente al sensor TCR5000.

### ¿Qué delay se necesita para tener al menos 20 muestras del evento?

Se necesitan al menos 20 muestras durante los 0.5 segundos que tarda la pieza en pasar.

Se realiza el cálculo:

0.5 s ÷ 20 muestras = 0.025 s

Por lo tanto:

0.025 s = 25 ms

El delay máximo sería de 25 ms.

### ¿Cuántas muestras da eso mientras la pieza pasa?

Con un delay de 20  se obtiene aproximadamente:

1000 ms ÷ 20 ms = 50 muestras por segundo

Como la pieza tarda aproximadamente 0.5 segundos:

0.5 s × 50 muestras/s = 25 muestras

Por lo tanto, se obtienen aproximadamente 25 muestras mientras la pieza pasa frente al sensor.

Esto supera las 20 muestras mínimas solicitadas.

### 4. Ajuste del delay en sensor.ino
el delay queda en 20 


### Semana 3 - Recolección de datos etiquetados (U2)
## Antes de clase 
## Bloque 1 

las columnas que son exactas de tu datos.csv, en el cual contene cada uno del nombre de cada unaa y que guarda:
ventana,P,Valor,Tipo

tus etiquetas, escritas tal cual como van a aparecer en el archivo:
Rojo,Blanco,Negro

cinco filas de ejemplo de tu tabla, con valores plausibles de tu sensor: 
523 blanco 
410 rojo 
85 negro 

## Bloque 2
- Cuántas ventanas por clase vas a capturar: 
30 por cada una de las clases 
- En qué orden: Blanco Rojo Negro 
- Cómo vas a mantener pareja la velocidad de la mano, en concreto: voy a marcar una linea de 15 cm, y mi sensor va a estra ubicado en 5cm. 
- A qué distancia del sensor va a pasar la pieza: aproximadamente a 3cm 

### Avance del proyecto
difinir las databases que se van a usar en cada uno de nuestros sensores y marcando las etiquetas que cada uno va a usar. 

### Semana 4 Limpieza y normalización de señales (U2)
### Antes de clase 
### bloque 1 
 
- ¿Qué tipo de ruido ves en tu señal y de dónde crees que viene? 
El sensor presentar pequeñas variaciones en las lecturas debido a interferencias eléctricas, cables,o cambios de luz del salon que interfieren en varias ocasiones. 
- Qué rango físico tiene tu sensor y qué valores estás descartando por imposibles.
El Arduino mide valores de 0 a 1023. Los valores fuera de este rango se consideran incorrectos y se eliminan.
- Qué tamaño de filtro elegiste y por qué, en relación con la duración de tu evento.
Se eligió un filtro de 5 muestras porque cada ventana tiene 200 muestras. Esto ayuda a reducir el ruido sin cambiar demasiado la señal.

### Bloque 2