
#include <Servo.h>

const int PIN_SENSOR = A0;
const int POS_REPOSO = 90;

Servo servo;

void setup() {
  Serial.begin(115200);
  servo.attach(9);
  servo.write(POS_REPOSO);
}

void loop() {
  // Enviar lectura del TCR5000 a Python
  Serial.println(analogRead(PIN_SENSOR));

  // Revisar si Python envió una orden
  if (Serial.available() > 0) {
    char orden = Serial.read();

    switch (orden) {
      case 'A':
        servo.write(45);   // Negro
        break;

      case 'B':
        servo.write(90);   // Rojo
        break;

      case 'C':
        servo.write(135);  // Blanco
        break;

      case '0':
        servo.write(POS_REPOSO);
        break;
    }
  }

  delay(10);
}
