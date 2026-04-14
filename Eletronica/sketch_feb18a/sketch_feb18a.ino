#include <SoftwareSerial.h>
#include <Arduino.h>

SoftwareSerial mySerial(13, 12);
unsigned char a;
unsigned char b[13];
unsigned char i, r;
void setup() {
  // put your setup code here, to run once:
  mySerial.begin(9600);
  Serial.begin(9600);
  Serial.println("Readly");
  //[85, 106, 172, 178, 254, 254, 254, 254, 254, 254, 254, 162]
}

void loop() {
  if (mySerial.available() >= 12) {  // Verifica se há 12 bytes disponíveis
    byte dados[12];                  // Array para armazenar os dados recebidos
    mySerial.readBytes(dados, 12);   // Lê 12 bytes da porta serial

    for (int i = 0; i < 12; i++) {
      int dado = dados[i];  // Converte o byte para inteiro
      if (i == 8) {         // Imprime o sexto elemento do array
        if (dado < 100) {
          Serial.println(dado);
        }
      }
    }
  }
}