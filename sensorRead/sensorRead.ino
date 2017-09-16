const int sensorPin = A3;
const int numSamples = 20;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int i = 0;
  int sum = 0;
  int avg = 0;
  
  for (i=0;i<numSamples;i++){
    int sensorVal = analogRead(sensorPin);
    sum += sensorVal;
  };
  
  avg = sum/numSamples;
  avg = map(avg,0,700,0,255);
  Serial.write(avg);
  // delay(300);
  
}
