# Bitácora del proyecto
## Semana 1 
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


## Semana  2 
### Antes de clase 
#### Bloque 1

 1. Que sensor vas a usar y que tipo de salida tiene: usare el sensor tcrt5000 el cual va a ser para detectar el color de los objectos y es de una salida analogica

 2. Tres líneas de ejemplo tal como se van a ver saliendo de tu Arduino, con valores plausibles para tu caso. 
 - 996
 - 1015
 - 1018

 3. Por qué el Arduino no puede mandar Serial.println("Leyendo...").
 El Arduino manda solo datos, nunca mensajes para humanos.

#### Bloque 2:

Para esta práctica se utilizó un sensor TCR5000 mediante su salida analógica (AO), conectada a la entrada A0 del Arduino.

1. ¿Cuánto tarda la pieza en cruzar frente al sensor?

Se estima que la pieza tarda aproximadamente 0.5 segundos en cruzar frente al sensor TCR5000.

2. ¿Qué delay se necesita para tener al menos 20 muestras del evento?

Se necesitan al menos 20 muestras durante los 0.5 segundos que tarda la pieza en pasar.

Se realiza el cálculo:

0.5 s ÷ 20 muestras = 0.025 s

Por lo tanto:

0.025 s = 25 ms

El delay máximo sería de 25 ms.

3. ¿Cuántas muestras da eso mientras la pieza pasa?

Con un delay de 20  se obtiene aproximadamente:

1000 ms ÷ 20 ms = 50 muestras por segundo

Como la pieza tarda aproximadamente 0.5 segundos:

0.5 s × 50 muestras/s = 25 muestras

Por lo tanto, se obtienen aproximadamente 25 muestras mientras la pieza pasa frente al sensor.

Esto supera las 20 muestras mínimas solicitadas.

4. Ajuste del delay en sensor.ino
el delay queda en 20 


## Semana 3 
### Antes de clase 
#### Bloque 1 

1. las columnas que son exactas de tu datos.csv, en el cual contene cada uno del nombre de cada unaa y que guarda:
ventana,P,Valor,Tipo

2. tus etiquetas, escritas tal cual como van a aparecer en el archivo:
Rojo,Blanco,Negro

3. cinco filas de ejemplo de tu tabla, con valores plausibles de tu sensor: 
523 blanco 
410 rojo 
85 negro 

#### Bloque 2
1. ¿Cuántas ventanas por clase vas a capturar?
30 por cada una de las clases 
2. ¿En qué orden? 
Blanco Rojo Negro 
3. ¿Cómo vas a mantener pareja la velocidad de la mano, en concreto? 
voy a marcar una linea de 15 cm, y mi sensor va a estra ubicado en 5cm. 
4. ¿A qué distancia del sensor va a pasar la pieza? 
Aproximadamente a 3cm 

### Avance del proyecto
difinir las databases que se van a usar en cada uno de nuestros sensores y marcando las etiquetas que cada uno va a usar. 

## Semana 4 
### Antes de clase 
#### bloque 1 
 
1. ¿Qué tipo de ruido ves en tu señal y de dónde crees que viene? 
El sensor presentar pequeñas variaciones en las lecturas debido a interferencias eléctricas, cables,o cambios de luz del salon que interfieren en varias ocasiones. 
2. ¿Qué rango físico tiene tu sensor y qué valores estás descartando por imposibles?
El Arduino mide valores de 0 a 1023. Los valores fuera de este rango se consideran incorrectos y se eliminan.
3. ¿Qué tamaño de filtro elegiste y por qué, en relación con la duración de tu evento?
Se eligió un filtro de 5 muestras porque cada ventana tiene 200 muestras. Esto ayuda a reducir el ruido sin cambiar demasiado la señal.

#### Bloque 2

1. ¿Cuánto se movió tu línea base entre la primera y la última ventana de la sesión?
La línea base se calculó utilizando el promedio de las primeras 20 muestras de cada ventana. Al comparar la primera y la última ventana hubo una deriva en la señal.
2. ¿Qué normalización elegiste y por qué?
Elegí la normalización Min-Max, porque las lecturas del sensor tienen un rango conocido y permite llevar los valores a un rango de 0 a 1, facilitando el procesamiento posterior del clasificador.
3. ¿Al comparar antes y después: ¿se parecen más entre sí las ventanas de una misma clase?
Después de corregir la línea base, las ventanas de una misma clase presentan formas más parecidas y comienzan cerca de un mismo nivel, ayudando a identificar las diferencias entre las piezas y no las variaciones. 

### Avance del proyecto

### Avance del proyecto

1. ¿Qué le hiciste a tu señal, en orden, y por qué en ese orden?
Primero se revisaron los datos obtenidos del sensor TCR5000 para eliminar valores inválidos. Después se aplicó un filtro de media móvil para reducir el ruido de las mediciones. Finalmente, se conservaron los valores de intensidad de cada color para mantener las diferencias entre blanco, rojo y negro, generando el archivo `datos_limpios.csv`.
2. ¿Qué tanto se parecen entre sí las ventanas de una misma clase después de limpiar, comparado con antes?**
Después de aplicar la limpieza, las señales de un mismo color presentan un comportamiento más uniforme y con menos variaciones de ruido. En comparación con las señales originales, las ventanas deberían mostrar mayor estabilidad, facilitando la identificación de las características de cada color.
3. Si dos de tus clases se traslapan, ¿qué vas a hacer al respecto?
Si las señales de dos colores presentan valores similares, se pueden revisar las condiciones de medición, como la iluminación y la distancia entre el sensor y la superficie. También se pueden capturar nuevas muestras y utilizar características temporales y espectrales para mejorar la clasificación de los colores.

## Semana 5
### Antes de clase 
#### Bloque 1 

| Característica      | ¿Por qué debería distinguir mis clases?                             |
| ------------------- | ------------------------------------------------------------------- |
| Media               | Permite conocer el valor promedio que genera cada color.            |
| Desviación estándar | Indica cuánto cambia la señal mientras el sensor detecta la pieza.  |
| Mínimo              | Puede mostrar qué tan baja llega la señal para cada color.          |
| Máximo              | Permite comparar el valor más alto producido por cada color.        |
| Rango               | Muestra la diferencia entre el valor máximo y mínimo de cada pieza. |
| Duración            | Indica cuánto tiempo permanece la pieza frente al sensor.           |

Predicción: Creo que el mínimo será la característica más útil porque cada color puede reflejar diferente cantidad de luz. La duración podría ser la menos útil porque depende de la velocidad con la que pase la pieza frente al sensor.

#### Bloque 2

1. ¿Cuántas filas y cuántas columnas quedó tu features.csv, y por qué ese número de filas?
El archivo features.csv quedó con 90 filas y 9 columnas. Las 90 filas corresponden a las ventanas obtenidas de las tres clases: Blanco, Negro y Rojo, y las columnas corresponden a las características calculadas de cada ventana.
2. ¿Qué par de características separa mejor tus clases, con la gráfica que lo muestra?
Al analizar el diagrama de dispersión de rango vs duración, se observa que estas características permiten diferenciar la clase Negro, pero no separan correctamente las clases Blanco y Rojo, ya que sus puntos se encuentran encimados. Por lo tanto, es necesario probar otros pares de características para encontrar una mejor separación entre las tres clases.
3. ¿Si hay dos clases que se encimen, ¿cuáles y qué vas a hacer?
Las clases Blanco y Rojo se encuentran encimadas en la gráfica de rango vs duración, debido a que presentan valores muy similares. Para mejorar la separación, se probarán otras características, como media vs energía y desviación estándar vs rango, con el objetivo de encontrar un par que permita distinguir mejor las tres clases.

### Avance del proyecto
Se empezo con la creacion de las piezas a usar para empezar a darles un color especifico para mas muestreos y que solo se base en una solo calidad de color y tomar mas muestras en diferentes entornos para mayor adquisicion de datos para tener menor cantidad de errores al momento de una variacion.

### Avance del proyecto

### Avance del proyecto

1. ¿Qué características te quedaste y cuáles descartaste? ¿Por qué?
Se conservaron características temporales como la media, desviación estándar, mínimo, máximo, rango, energía y duración. También se incluyeron características espectrales como la frecuencia dominante, el centroide espectral y la energía por bandas. No se descartaron características en esta etapa, ya que se utilizaron para evaluar cuáles aportaban más información a la clasificación.
2. ¿Cuál característica separa mejor tus clases? ¿Coincidió con lo que predijiste en el bloque 1?
La media de los valores del sensor fue una de las características más útiles para diferenciar los colores blanco, rojo y negro, debido a sus distintos niveles de reflexión infrarroja. Esto coincidió con lo esperado en el bloque 1, donde se había previsto que la intensidad de la señal permitiría distinguir los colores.
3. Si tuviste que recapturar, ¿qué cambiaste y qué mejoró?
Se completó la captura de 90 ventanas, obteniendo 30 muestras por cada color. También se corrigió el procesamiento para conservar los valores absolutos de la señal y evitar que la normalización eliminara las diferencias entre colores. Esto permitió generar un conjunto de características más adecuado para entrenar el clasificador KNN.

## Semana 6 
### Antes de clase 
#### Bloque 1 

1. Tu frecuencia de muestreo (la que quedó en tu sensor.ino después de la semana 2)
Mi frecuencia de muestreo es de 100 Hz, porque el sensor toma aproximadamente 100 muestras por segundo.
2. Tu frecuencia de Nyquist, y qué significa para tu señal.
Mi frecuencia de Nyquist es de 50 Hz. Esto significa que solo puedo analizar correctamente frecuencias de hasta 50 Hz. Las frecuencias mayores pueden producir aliasing y aparecer como frecuencias falsas más bajas.
3. Tu resolución con el largo de ventana que usas. 
Mi ventana tiene 200 muestras, por lo tanto:
Δf = 100 Hz / 200 = 0.5 Hz. Esto significa que el espectro mostrará información cada 0.5 Hz. 
4. Tu predicción: ¿esperas que tus clases se distingan en frecuencia? ¿Por qué sí o por qué no?
Espero que las clases blanco, rojo y negro puedan presentar diferencias en frecuencia, porque cada color produce una respuesta diferente en el TCR5000 y las variaciones de la señal pueden cambiar entre cada clase. Sin embargo, es posible que la diferencia principal esté en la intensidad de la señal y no tanto en su frecuencia.

#### Bloque 2

1. ¿Qué frecuencia dominante tiene tu señal y tiene sentido físico?
La frecuencia dominante de la señal analizada es aproximadamente 4.5 Hz. Esto representa una de las variaciones principales que detectó el sensor TCR5000 y puede relacionarse con cambios en la lectura durante la medición.
2. ¿Las características de frecuencia permiten distinguir entre blanco, rojo y negro?
Por el momento no es posible determinarlo, ya que las gráficas solamente muestran datos correspondientes al color negro. Es necesario analizar muestras de los otros dos colores para realizar una comparación.
3. ¿Conviene conservar las características espectrales o eliminarlas? ¿Por qué?
Por ahora conviene conservarlas para continuar el análisis. Una vez que se tengan muestras de los tres colores, se podrá determinar si estas características ayudan a diferenciarlos o si es mejor eliminarlas.

### Avance del proyecto

### Avance del proyecto

1. ¿La frecuencia te sirvió o no? Explica físicamente por qué.
Las características de frecuencia sirvieron como información complementaria para analizar las variaciones de las señales del sensor TCR5000. Sin embargo, la principal diferencia entre los colores se encuentra en la intensidad de la luz infrarroja reflejada, por lo que las características temporales, especialmente la media, resultan más importantes para distinguir blanco, rojo y negro.
2. ¿Cuál es la lista final de características con las que vas a entrenar?
Se seleccionaron 13 características para el entrenamiento del clasificador KNN:
- Temporales:media, desviación estándar, mínimo, máximo, rango, energía y duración.
- Espectrales:frecuencia dominante, energía espectral, centroide espectral, banda baja, banda media y banda alta.
Estas características permiten describir tanto la intensidad como las variaciones de las señales obtenidas del sensor.
3. ¿Cómo se ve la separación de tus clases con el conjunto final? ¿Qué tan bien predices que funcionará el clasificador?
Las clases presentan una separación favorable debido a las diferencias de intensidad registradas por el sensor TCR5000. Se espera que el clasificador KNN consiga una exactitud alta, aunque podrían presentarse pequeñas confusiones entre los colores rojo y blanco debido a la similitud de algunas mediciones.

## Semana 7
### Antes de clase 
#### Bloque 1 

1. ¿Con cuántos ejemplos vas a entrenar y con cuántos a probar?
Actualmente cuento con una ventana de datos correspondiente al color negro. Por el momento no es posible dividir los datos en entrenamiento y prueba, ya que necesito más muestras de los tres colores.
Mi objetivo es recolectar 90 ventanas, distribuidas en 30 de color negro, 30 de rojo y 30 de blanco. Una vez completadas, utilizaré 72 ventanas para entrenamiento (80%) y 18 para prueba (20%).
2. ¿Qué algoritmo eliges para empezar y por qué?
Elegiré el algoritmo de árbol de decisión porque permite clasificar las piezas mediante las características obtenidas del sensor TCR5000. Además, es fácil de interpretar, no requiere estandarizar los datos y permite identificar las reglas que utiliza para diferenciar los colores negro, rojo y blanco.
3. ¿Por qué un modelo que acierta el 100% en entrenamiento puede ser inútil?
Porque puede memorizar los datos de entrenamiento sin aprender a identificar correctamente piezas nuevas. Aunque obtenga un 100% de aciertos con los datos que ya conoce, puede equivocarse cuando se le presenten muestras diferentes. Por eso es importante evaluar el modelo con datos que no haya utilizado durante el entrenamiento.

#### Bloque 2

1. ¿Cuál fue tu exactitud en el conjunto de prueba?
Se obtuvo una exactitud del 95.65 % en el conjunto de prueba, logrando clasificar correctamente 22 de las 23 muestras evaluadas. Esto demuestra que el modelo KNN tiene un buen desempeño para identificar los colores blanco, rojo y negro mediante el sensor TCR5000.
2. ¿Qué par de clases se confunde más?
Las clases que presentaron confusión fueron rojo y blanco, ya que una muestra correspondiente al color rojo fue clasificada incorrectamente como blanco. Los demás colores se identificaron correctamente, como se observa en la matriz de confusión.
3. ¿El resultado coincidió con lo que predijiste en la Semana 6?
Sí, los resultados coincidieron con lo esperado en la Semana 6, ya que anteriormente se habían observado diferencias en los valores registrados por el sensor TCR5000 para cada color. Al entrenar el clasificador KNN, se obtuvo una exactitud del 95.65 %, lo que confirma que las características de las señales permiten distinguir los tres colores con buenos resultados en las muestras evaluadas.

### Avance del proyecto

## Semana 7 — Entrenamiento del clasificador

Algoritmo seleccionado: K-Nearest Neighbors (KNN).

Objetivo:Clasificar los colores blanco, rojo y negro utilizando las características temporales y espectrales obtenidas del sensor TCR5000.

Configuración del modelo:
- Algoritmo: KNN.
- Número de vecinos (K): pendiente de verificar en `entrenar.py`.
- Escalado de características: verificar configuración del `StandardScaler`.
- Características utilizadas: 13.
- Total de ventanas: 90.
- Entrenamiento: 67 ventanas.
- Prueba: 23 ventanas.

Resultados:
- Exactitud en entrenamiento: pendiente de calcular.
- Exactitud en prueba: 95.65 %.
- Predicciones correctas: 22.
- Predicciones incorrectas: 1.
- Principal confusión: rojo clasificado como blanco.

Archivos:
- `datos/features.csv`: características para el entrenamiento.
- `modelo.pkl`: modelo entrenado.
- `figuras/confusion.png`: matriz de confusión.

Es necesario validar el modelo con nuevas capturas independientes para comprobar su capacidad de generalización.

## Semana 8
### Antes de clase 
#### Bloque 1 