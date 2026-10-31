
#include <Servo.h>

const int PIN_SENSOR = A0;
const int PIN_SERVO = 9;
const int POS_REPOSO = 90;

Servo servo;

void setup() {
  Serial.begin(115200);

  servo.attach(PIN_SERVO);
  servo.write(POS_REPOSO);
  delay(500);
}

void loop() {
  // Enviar lectura del sensor TCRT5000 a Python
  int lectura = analogRead(PIN_SENSOR);
  Serial.println(lectura);

  // Revisar si Python envio una orden
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

