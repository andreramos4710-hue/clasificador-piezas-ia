
// sensor.ino
// Sensor TCR5000 para clasificador de piezas por color
// Arduino -> Python
//
// Formato de salida:
// Un valor numérico por línea
//
// Colores que se utilizarán en Python:
// blanco, rojo y negro

const int PIN_TCR5000 = A0;

void setup() {
  // Comunicación con Python
  Serial.begin(115200);

  // Pequeña pausa para estabilizar el sensor
  delay(500);
}

void loop() {

  // Leer el valor analógico del TCR5000
  int valor = analogRead(PIN_TCR5000);

  // Enviar SOLO el valor numérico
  // Python utilizará este dato para crear
  // las ventanas de 200 muestras
  Serial.println(valor);

  // 10 ms = aproximadamente 100 muestras por segundo
  delay(10);
}
