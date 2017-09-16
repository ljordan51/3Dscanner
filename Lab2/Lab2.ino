#include <Servo.h>

const byte panPin = 8;
const byte tiltPin = 9;
const byte sensorPin = 3;
const byte step = 3;
const byte panMin = 42;
const byte panMax = 132;
const byte tiltMin = 30;
const byte tiltMax = 120;
const int delayTime = 180;

Servo pan;
Servo tilt;

void setup() {
  Serial.begin(9600);
  pan.attach(panPin, 570, 2380);
  tilt.attach(tiltPin, 550, 2280);
  pan.write((panMin+panMax)/2);
  tilt.write((tiltMin+tiltMax)/2);
  delay(1000);
}

void loop() {
  while(!Serial.available()){
    pan.write((panMin+panMax)/2);
    tilt.write((tiltMin+tiltMax)/2);
  }
  while(Serial.available()){
    Serial.read();
    delay(5);
  }

  pan.write(panMin);
  tilt.write(tiltMin);
  delay(700);
  bool scanDir = 1;
  for(byte i = panMin; i <= panMax; i += step){
    pan.write(i);
    delay(delayTime);
    if(scanDir){
      for(byte j = tiltMin; j <= tiltMax; j += step){
        tilt.write(j);
        delay(delayTime);
        measureSend(i, j);
      }
    }
    else{
      for(int j = tiltMax; j >= tiltMin; j -= step){
        tilt.write(j);
        delay(delayTime);
        measureSend(i, j);
      }
    }
    scanDir = !scanDir;
  }
}

void measureSend(byte x, byte y){
  int dist = analogRead(sensorPin);
  byte data[6];
  data[0] = x;
  data[1] = y;
  data[2] = dist & 255;
  data[3] = (dist >> 8)  & 255;
  data[4] = (dist >> 16) & 255;
  data[5] = (dist >> 24) & 255;
  Serial.write(data, 6);
}
