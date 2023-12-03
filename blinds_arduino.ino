// Exposes a light sensor and servo motor over serial ()
// Written by Collin Conrad

#include <Servo.h>

#define LDR_PIN A0
#define SERVO_PIN 9

const float FILTER_FACTOR = 0.05;
const unsigned long LDR_RESEND_DELAY = 2000; // Every 2 seconds

Servo blindActuator;

bool ldrLastReportedState = false;
unsigned long ldrLastSent = 0;

float sensorSmoothed = 0;

void setup() {
  Serial.begin(9600);
  blindActuator.attach(SERVO_PIN);
}

void loop() {
  while(Serial.available()) {
    int inByte = Serial.read();

    if(inByte == 'o')
      blindActuator.write(180);
    else if(inByte == 'c')
      blindActuator.write(0);
  }

  int sensorValue = analogRead(A0);

  sensorSmoothed += ((float) sensorValue - sensorSmoothed) * FILTER_FACTOR;

  bool isLDRTriggered = sensorSmoothed >= 500;

  if(isLDRTriggered != ldrLastReportedState || millis() - ldrLastSent >= LDR_RESEND_DELAY) {
    ldrLastReportedState = isLDRTriggered;
    ldrLastSent = millis();

    Serial.print(isLDRTriggered ? 'l' : 'd');
  }

  delay(10);
}
