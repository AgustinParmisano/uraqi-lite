#include <DHT.h>

#define DHTPIN 7
#define DHTTYPE DHT11
#define tierra A5
#define luz A0

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float m = analogRead(tierra);

  delay(1000);
  //Serial.print("Tierra: ");
  Serial.print(m);
  if (isnan(t) || isnan(h) ) {
    Serial.println("00 ");
  } else {
    //Serial.print("Temperatura: ");
    Serial.print(t);
    //Serial.print("Humedad: ");
    Serial.print(h);
  }
  Serial.println("");
}
