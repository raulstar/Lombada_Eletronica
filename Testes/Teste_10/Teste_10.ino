
//#include <Adafruit_NeoPixel.h>
#include <SoftwareSerial.h>
#include <FastLED.h>
#define PIN 2       // On Trinket or Gemma, suggest changing this to 1
#define LED_PIN 10  // Popular NeoPixel ring size
#define DELAYVAL 1  // Time (in milliseconds) to pause between pixels
#define NUM_LEDS 50
#define DATA_PIN 4

#define um 3
#define alerta 2
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// variáveis
int vermelho = 255;
int verde = 0;
int azul = 255;
int velocidade = 0;
unsigned char a;
unsigned char b[13];
int dado;
int comtador;
int temp = 0;
char seguimento;
int brightness = 255;

//Adafruit_NeoPixel pixels(LED_PIN, PIN, NEO_GRB + NEO_KHZ800);
CRGB leds[NUM_LEDS];
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// prototipo Funções

void Unidade(int nun);
void Decodifica(int numero);
void Seguimento(bool multiplo, char s);
SoftwareSerial mySerial(3, 2);
void contaTempo(void);
void Numero(int);
void Radar(void);
bool Manual(void);
void Envia(void);

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
  //pixels.begin();  // INITIALIZE NeoPixel strip object (REQUIRED)
  FastLED.addLeds<WS2812, DATA_PIN>(leds, NUM_LEDS);
  FastLED.setBrightness(brightness);
  FastLED.clear();

  for (int i = 0; i < 4; i++)
    pinMode(portas1[i], OUTPUT);

  for (int j = 0; j < 4; j++)
    pinMode(portas2[j], OUTPUT);
  mySerial.begin(9600);
  Serial.begin(115200);
  Serial.println("Pronto");
  Numero(88);
  digitalWrite(alerta, HIGH);
  digitalWrite(um, HIGH);
  //digitalWrite(um, HIGH);
  delay(800);
  Numero(0);
  digitalWrite(um, LOW);
  digitalWrite(alerta, LOW);
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Loop Principal
void loop() {
  //Unidade(1);
  //seguimento = 'a';
  Seguimento(0, 'a');
  delay(400);
  //leds[3] = CRGB::Red;
  //FastLED.clear();
  //Decodifica(22);
  Radar();
  contaTempo();
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
void Seguimento(int multiplo, char s) {
  int digito = 0;
  if (multiplo) digito = 70;
  switch (s) {

    case 'a':
      for (int i = 0; i < 10; i++) {
        leds[i + digito] = CRGB(azul, verde, vermelho);
        //Serial.print(i);
        FastLED.show();
        delay(velocidade);
        ;
      }
      break;

    case 'b':
      for (int i = 10; i < 20; i++) {
        leds[i + digito] = CRGB(azul, verde, vermelho);
        //Serial.print(i);
        FastLED.show();
        delay(velocidade);
      }
      break;

    case 'c':
      for (int i = 20; i < 30; i++) {
        leds[i + digito] = CRGB(azul, verde, vermelho);
        FastLED.show();
        //delay(velocidade);
      }
      break;
    case 'd':
      for (int i = 30; i < 40; i++) {
        leds[i + digito] = CRGB(azul, verde, vermelho);
        FastLED.show();
        delay(velocidade);
      }
      break;
    case 'e':
      for (int i = 40; i < 50; i++) {
        leds[i + digito] = CRGB(azul, verde, vermelho);
        FastLED.show();
        delay(velocidade);
      }
      break;
    case 'f':
      for (int i = 50; i < 60; i++) {
        leds[i + digito] = CRGB(azul, verde, vermelho);
        FastLED.show();
        delay(velocidade);
      }
      break;
    case 'g':
      for (int i = 60; i < 70; i++) {
        leds[i + digito] = CRGB(azul, verde, vermelho);
        FastLED.show();
        delay(velocidade);
      }
      break;
    case 'h':
      for (int i = 140; i < 160; i++) {
        leds[i + digito] = CRGB(azul, verde, vermelho);
        FastLED.show();
        delay(velocidade);
      }
      break;
  }
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
void Decodifica(int numero) {
  int dezena = numero / 10;
  int unidade = numero % 10;
  int multiplo = 0;
  int varredura = 2;
  numero = unidade;
  // Serial.print(numero);
  //Serial.print('unidade',unidade);

  for (int i = 0; i < varredura; i++) {
    int digito = unidade;
    switch (numero) {
      case 0:
        Seguimento(multiplo, 'a');
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'c');
        Seguimento(multiplo, 'd');
        Seguimento(multiplo, 'e');
        Seguimento(multiplo, 'f');
        FastLED.show();
        break;
      case 1:
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'c');
        FastLED.show();
        break;
      case 2:
        Seguimento(multiplo, 'a');
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'd');
        Seguimento(multiplo, 'e');
        Seguimento(multiplo, 'g');
        FastLED.show();
        break;
      case 3:
        Seguimento(multiplo, 'a');
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'c');
        Seguimento(multiplo, 'd');
        Seguimento(multiplo, 'g');
        FastLED.show();
        break;
      case 4:
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'c');
        FastLED.show();
        break;
      case 5:
        Seguimento(multiplo, 'a');
        Seguimento(multiplo, 'c');
        Seguimento(multiplo, 'd');
        Seguimento(multiplo, 'f');
        Seguimento(multiplo, 'g');
        FastLED.show();
        break;
      case 6:
        Seguimento(multiplo, 'a');
        Seguimento(multiplo, 'c');
        Seguimento(multiplo, 'd');
        Seguimento(multiplo, 'e');
        Seguimento(multiplo, 'f');
        Seguimento(multiplo, 'g');
        break;
      case 7:
        Seguimento(multiplo, 'a');
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'c');
        FastLED.show();
        break;
      case 8:
        Seguimento(multiplo, 'a');
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'c');
        Seguimento(multiplo, 'd');
        Seguimento(multiplo, 'e');
        Seguimento(multiplo, 'f');
        Seguimento(multiplo, 'g');
        FastLED.show();
        break;
      case 9:
        Seguimento(multiplo, 'a');
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'c');
        Seguimento(multiplo, 'd');
        Seguimento(multiplo, 'f');
        Seguimento(multiplo, 'g');
        FastLED.show();
        break;
        FastLED.show();
        break;
    }
    if (dezena > 0) {
      multiplo = 1;
      numero = dezena;
      varredura = dezena;
    }
  }
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
void Envia() {


  int value = 0;
  int previous_millis = 25;
  int loop_time = 87;

  // escreve o resultado
  if (Serial.availableForWrite()) {
    String outstr = String(String(dado, DEC) + "," + String(loop_time, DEC) + "," + String(value, DEC));
    Serial.println(outstr);
  }
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
            //Serial.print("Vel. ");
            Envia();
            //Serial.println(dado);
            //envia = String(dado, DEC);
            //Serial.println(envia);
            Numero(dado);
            if (dado > 20) {
              digitalWrite(alerta, HIGH);
              //Serial.println("auto");
              //Serial.println(" ");
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
    //digitalWrite(alerta, LOW);
    //Serial.println("Zero");
  }
}
