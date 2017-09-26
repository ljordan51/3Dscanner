#include <Servo.h>

// pins hardware is connected to
const byte panPin = 8;
const byte tiltPin = 9;
const byte sensorPin = 3;

const byte step = 1; // resolution, in degrees

// scan angle ranges
const byte panMin = 42;
const byte panMax = 132;
const byte tiltMin = 30;
const byte tiltMax = 120;

const int delayTime = 180; // time to wait for servo before reading distance

Servo pan; // name servos
Servo tilt;

void setup() {
  Serial.begin(9600); // start serial comms
  pan.attach(panPin, 570, 2380); // pulse width values are calibrated per servo
  tilt.attach(tiltPin, 550, 2280);
  pan.write((panMin+panMax)/2); // send the servos to straight ahead
  tilt.write((tiltMin+tiltMax)/2);
  delay(700); // wait for them to get there
}

void loop() {
  Serial.println("Arduino ready!");
  while(!Serial.available()){ // keep servos straight ahead until something is sent to serial port
    pan.write((panMin+panMax)/2);
    tilt.write((tiltMin+tiltMax)/2);
  }
  while(Serial.available()){
    Serial.read();
    delay(5);
    // read from serial buffer until empty
  }

  pan.write(panMin); // go to start position
  tilt.write(tiltMin);
  delay(700);  // wait for servos to reach start position
  bool scanDir = 1; // keep track of whether scanning up or down
  for(byte i = panMin; i <= panMax; i += step){ // cycle through horizontal range
    pan.write(i);
    delay(delayTime);
    if(scanDir){
      for(byte j = tiltMin; j <= tiltMax; j += step){ // cycle up through vertical range
        tilt.write(j);
        delay(delayTime);
        measureSend(i, j);
      }
    }
    else{
      for(int j = tiltMax; j >= tiltMin; j -= step){ // cycle down through vertical range
        tilt.write(j);
        delay(delayTime);
        measureSend(i, j);
      }
    }
    scanDir = !scanDir; // switch vertical scan direction
  }
  byte end[] = {255,255,255,255,255,255};
  Serial.write(end,6);  // tell python that scan is finished
}

void measureSend(byte x, byte y){ // read distance and send over serial
  int dist = analogRead(sensorPin); // read distance
  byte data[6];
  int panRange = panMax - panMin;
  int tiltRange = tiltMax - tiltMin;
  data[0] = map(x, panMin, panMax, 0, panRange); // first byte is pan
  data[1] = map(y, tiltMin, tiltMax, 0, tiltRange); // second byte is tilt
  // convert the distance (int) to four bytes
  data[2] = dist & 255;
  data[3] = (dist >> 8)  & 255;
  data[4] = (dist >> 16) & 255;
  data[5] = (dist >> 24) & 255;
  Serial.write(data, 6); // send data
}
