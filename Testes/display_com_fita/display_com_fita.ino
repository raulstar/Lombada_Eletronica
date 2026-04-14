
#include <Adafruit_NeoPixel.h>
#define PIN 13          // On Trinket or Gemma, suggest changing this to 1
#define NUMPIXELS 140  // Popular NeoPixel ring size
#define DELAYVAL 1     // Time (in milliseconds) to pause between pixels

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

int vermelho = 0;
int verde = 255;
int azul = 0;
int velocidade = 0;

char seguimento;

void Unidade(int nun);
void Decodifica(int numero);
void Seguimento(bool multiplo, char s);

void setup() {
  pixels.begin();  // INITIALIZE NeoPixel strip object (REQUIRED)
  Serial.begin(9600);
}

void loop() {
  //Unidade(1);
  //seguimento = 'a';
  //Seguimento(seguimento);
  Decodifica(23);
}

void Seguimento(int multiplo, char s) {
  int digito = 0;
  if (multiplo) digito = 70;
  switch (s) {

    case 'a':
      for (int i = 0; i < 10; i++) {
        pixels.setPixelColor(i + digito, pixels.Color(azul, verde, vermelho));
        //pixels.show();
        //delay(velocidade);
      }
      break;

    case 'b':
      for (int i = 10; i < 20; i++) {
        pixels.setPixelColor(i + digito, pixels.Color(azul, verde, vermelho));
        //pixels.show();
        //delay(velocidade);
      }
      break;

    case 'c':
      for (int i = 20; i < 30; i++) {
        pixels.setPixelColor(i + digito, pixels.Color(azul, verde, vermelho));
        //pixels.show();
        //delay(velocidade);
      }
      break;
    case 'd':
      for (int i = 30; i < 40; i++) {
        pixels.setPixelColor(i + digito, pixels.Color(azul, verde, vermelho));
        //pixels.show();
        delay(velocidade);
      }
      break;
    case 'e':
      for (int i = 40; i < 50; i++) {
        pixels.setPixelColor(i + digito, pixels.Color(azul, verde, vermelho));
        //pixels.show();
        delay(velocidade);
      }
      break;
    case 'f':
      for (int i = 50; i < 60; i++) {
        pixels.setPixelColor(i + digito, pixels.Color(azul, verde, vermelho));
        //pixels.show();
        delay(velocidade);
      }
      break;
    case 'g':
      for (int i = 60; i < 70; i++) {
        pixels.setPixelColor(i + digito, pixels.Color(azul, verde, vermelho));
        //pixels.show();
        delay(velocidade);
      }
      break;
    case 'h':
      for (int i = 140; i < 160; i++) {
        pixels.setPixelColor(i + digito, pixels.Color(azul, verde, vermelho));
        pixels.show();
        delay(velocidade);
      }
      break;
  }
}

void Decodifica(int numero) {
  int dezena = numero / 10;
  int unidade = numero % 10;
  int multiplo = 0;
  int varredura = 2;
  numero = unidade;
  Serial.print(numero);
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
        pixels.show();
        break;
      case 1:
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'c');
        pixels.show();
        break;
      case 2:
        Seguimento(multiplo, 'a');
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'd');
        Seguimento(multiplo, 'e');
        Seguimento(multiplo, 'g');
        pixels.show();
        break;
      case 3:
        Seguimento(multiplo, 'a');
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'c');
        Seguimento(multiplo, 'd');
        Seguimento(multiplo, 'g');
        pixels.show();
        break;
      case 4:
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'c');
        pixels.show();
        break;
      case 5:
        Seguimento(multiplo, 'a');
        Seguimento(multiplo, 'c');
        Seguimento(multiplo, 'd');
        Seguimento(multiplo, 'f');
        Seguimento(multiplo, 'g');
        pixels.show();
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
        pixels.show();
        break;
      case 8:
        Seguimento(multiplo, 'a');
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'c');
        Seguimento(multiplo, 'd');
        Seguimento(multiplo, 'e');
        Seguimento(multiplo, 'f');
        Seguimento(multiplo, 'g');
        pixels.show();
        break;
      case 9:
        Seguimento(multiplo, 'a');
        Seguimento(multiplo, 'b');
        Seguimento(multiplo, 'c');
        Seguimento(multiplo, 'd');
        Seguimento(multiplo, 'f');
        Seguimento(multiplo, 'g');
        pixels.show();
        break;
        pixels.show();
        break;
    }
    if (dezena > 0) {
      multiplo = 1;
      numero = dezena;
      varredura = dezena;
    }
  }
}
