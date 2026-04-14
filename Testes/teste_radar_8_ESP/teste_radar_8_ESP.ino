#include <SoftwareSerial.h>

#define um 3
#define alerta 2
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// variáveis
byte TX_PIN = 4;      // D2 - DI (Transmit Pin)
byte RX_PIN = 5;      // D1 - RO (Receive Pin)
byte DE_RE_PIN = 16;  // D0 - DE/RE (Data Enable/Receiver Enable Pin)
byte LED_PIN = 14;    // D5 - LED Pin

int dado;
unsigned char a;
unsigned char b[13];
int comtador;
int temp = 0;

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// prototipo Funções
SoftwareSerial mySerial(RX_PIN, TX_PIN);

void Radar(void);

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  pinMode(DE_RE_PIN, OUTPUT);
  digitalWrite(DE_RE_PIN, LOW);  // Enable RS485 Receiver mode
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);  // Turn off the LED initially
  Serial.println("\n");
  Serial.println("**** Receiver Started ****\n");
}

void loop() {
  Radar();
}

/////////////////////////////////////////////////////////////////////////////////////////
void Radar(void) {

  while (mySerial.available() >= 12) {  // Verifica se há 12 bytes disponíveis
    byte dados[12];                        // Array para armazenar os dados recebidos
    mySerial.readBytes(dados, 12);      // Lê 12 bytes da porta serial

    if (dados[1] == 85) {
      Serial.print("dado = ");
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