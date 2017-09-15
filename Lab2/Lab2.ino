#include <Servo.h>

const byte panPin = 8;
const byte tiltPin = 9;
const byte sensorPin = 3;
const byte step = 10;

Servo pan;
Servo tilt;

void setup() {
  Serial.begin(9600);
  pan.attach(panPin, 570, 2380);
  tilt.attach(tiltPin, 550, 2280);
  pan.write(0);
  tilt.write(0);

}

void loop() {
  delay(700);
  for(int i = 0; i <= 180; i += step){
    pan.write(i);
    delay(700);
    for(int j = 0; j <= 180; j += step){
      tilt.write(j);
      delay(200);
      dist = analogRead(sensorPin)
      byte data[6];
      data[0] = i;
      data[1] = j;
      data[2] = dist & 255;
      data[3] = (dist >> 8)  & 255;
      data[4] = (dist >> 16) & 255;
      data[5] = (dist >> 24) & 255;
      Serial.write(data, 6);
    }
    tilt.write(0);
  }
}
