#include <SoftwareSerial.h>
//#include <Arduino.h>

#define um 3
#define alerta 2
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// variáveis
unsigned char a;
unsigned char b[13];
int dado;
int comtador;
int temp = 0;

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// prototipo Funções
SoftwareSerial mySerial(13, 12);
void contaTempo(void);
void Numero(int);
void Radar(void);
bool Manual(void);

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

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Confiruração
void setup() {

  for (int i = 0; i < 4; i++)
    pinMode(portas1[i], OUTPUT);

  for (int j = 0; j < 4; j++)
    pinMode(portas2[j], OUTPUT);
  mySerial.begin(9600);
  Serial.begin(9600);
  Serial.println("Pronto");
  Numero(88);
  digitalWrite(alerta, HIGH);
  digitalWrite(um, HIGH);
  //digitalWrite(um, HIGH);
  delay(1000);
  Numero(0);
  digitalWrite(um, LOW);
  digitalWrite(alerta, LOW);
  //[85, 106, 172, 178, 254, 254, 254, 254, 254, 254, 254, 162]
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Loop Principal
void loop() {

  // Numero(dado);
  Radar();
  contaTempo();
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

  while (mySerial.available() >= 12) {  // Verifica se há 12 bytes disponíveis
    byte dados[12];                     // Array para armazenar os dados recebidos
    mySerial.readBytes(dados, 12);      // Lê 12 bytes da porta serial

    if (dados[1] == 85) {
      //Serial.print("dado = ");
      //Serial.println(dado);
      for (int i = 0; i < 12; i++) {
        dado = dados[i];  // Converte o byte para inteiro
        //Serial.print(dado);
        //Serial.print(" ");
        if (i == 6) {  // Imprime o sexto elemento do array
          Serial.print("dado ");
          Serial.print(dado);
          Serial.println("");
          if ((temp == 0) || (temp < dado)) {
            temp = dado;
            Serial.print("Vel. ");
            Serial.print(dado);
            Numero(dado);
            if (dado > 20) {
              digitalWrite(alerta, HIGH);
              Serial.println("auto");
              Serial.println(" ");
            }
          }
        }
      }
    }
    //Serial.println("");
  }
}
/////////////////////////////////////////////////////////////////////////////////////////
void contaTempo() {
  static unsigned long lastTime1 = 0;
  unsigned long currentTime = millis();  // guarda o tempo atual
  static unsigned long intevaloDeContagem = 5000;

  if ((currentTime - lastTime1) >= intevaloDeContagem) {  // verifica se já passaram 500ms desde a última mudança
    lastTime1 = currentTime;
    comtador++;
    Numero(0);
    temp = 0;
    digitalWrite(alerta, LOW);
    Serial.println("Zero");
  }
}
