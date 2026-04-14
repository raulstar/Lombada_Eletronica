#include <SoftwareSerial.h>
#include <Arduino.h>
//////////////////////////////////////////////////////////////////////////////////////////
SoftwareSerial mySerial(13, 12);
unsigned char a;
unsigned char b[13];
//unsigned char i, r;
int dado;


byte portas1[] = { 11, 10, 9, 8 };
byte portas2[] = { 7, 6, 5, 4 };
byte num[10][4] = {
  { 0, 0, 0, 0 },
  { 0, 0, 0, 1 },
  { 0, 0, 1, 0 },
  { 0, 0, 1, 1 },
  { 0, 1, 0, 0 },
  { 0, 1, 0, 1 },
  { 0, 1, 1, 0 },
  { 0, 1, 1, 1 },    
  { 1, 0, 0, 0 },
  { 1, 0, 0, 1 }
};
/////////////////////////////////////////////////////////////////////////////////////////
void Numero(int);
void Radar(void);
/////////////////////////////////////////////////////////////////////////////////////////
void setup() {

  for (int i = 0; i < 4; i++)
    pinMode(portas1[i], OUTPUT);

  for (int j = 0; j < 4; j++)
    pinMode(portas2[j], OUTPUT);
  mySerial.begin(9600);
  Serial.begin(9600);
  Serial.println("Pronto");
  Numero(88);
  delay(500);
  Numero(0);
  //[85, 106, 172, 178, 254, 254, 254, 254, 254, 254, 254, 162]
}
/////////////////////////////////////////////////////////////////////////////////////////
void loop() {

  //Numero(0);
  Radar();
}
/////////////////////////////////////////////////////////////////////////////////////////
void Numero(int valor) {
  int dezena = valor / 10;
  int unidade = valor % 10;

  for (int i = 0; i < 4; i++) {
    digitalWrite(portas1[i], num[dezena][i]);
    digitalWrite(portas2[i], num[unidade][i]);
  }
}
/////////////////////////////////////////////////////////////////////////////////////////
void Radar(void) {

  if (mySerial.available() >= 12) {  // Verifica se há 12 bytes disponíveis
    byte dados[12];                  // Array para armazenar os dados recebidos
    mySerial.readBytes(dados, 12);   // Lê 12 bytes da porta serial
    if (dado < 254)
      Serial.println(dado);
    for (int i = 0; i < 12; i++) {
      dado = dados[i];  // Converte o byte para inteiro
      if (i == 8) {     // Imprime o sexto elemento do array
        if (dado < 200) {
          dado = dado / 5;
          Serial.println(dado);
          Numero(dado);
          delay(1000);
        }
      }
    }
  }
}

/////////////////////////////////////////////////////////////////////////////////////////