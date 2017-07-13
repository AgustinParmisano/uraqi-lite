#include <DHT.h>

#define DHTTYPE DHT11
#define DHTPIN 7
#define luz A1

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200); //9600);
  dht.begin();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float l = analogRead(luz);

  delay(1000);
  
  //Serial.print("Luz: ");
  l = map(l, 0, 1023, 0, 100); 
  
  Serial.print(l);
  if (isnan(t) || isnan(h) ) {
    //Serial.println("00 ");
  } else {
    //Serial.print("Temperatura: ");
    Serial.print(t);
    //Serial.print("Humedad: ");
    Serial.print(h);
  }
  Serial.println("");
}
