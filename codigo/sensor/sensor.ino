// sensor.ino - envia la lectura del sensor por el puerto serial
// Formato: un valor por linea. Sin mensajes de texto.

const int PIN_TCR5000 = A0;

void setup() {
  Serial.begin(115200);
}

void loop() {

  int valor = analogRead(PIN_TCR5000);

  Serial.println(valor);

  delay(20);   // 20 ms -> 50 muestras por segundo
}