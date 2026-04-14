
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                        Lombada eletrônica
//
//   build 18/03/2025 by Raul
//  v0.7
//  Arduino IDE 2.3.3
//  platform = atmelavr
//  board = nanoatmega328
//  framework = Arduino IDE 2.3.3
//       @site:www.autorobotica.sp@gmail.com
//       @email: raulstar3@gmail.com ,
//       www.linkedin.com/in/raulstar/, Instagram: @raulstar3,github.com/raulstar
//
//  consiste em um radar de microondas LDS 306s de  21,1 GHz, e se comunica com o Arduino NANO atmega328p via interface RS 485,
//  usando uma fita LED interessada ws2811, são emulados um display de 7 segmento que exibe a velocidade.
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// mapeamento de hardware
#include <SoftwareSerial.h>  //1.0
#include <FastLED.h>         //FastLED 3.9.15
#define NUM_LEDS 67
#define DATA_PIN 4
#define um 3
#define alerta 2
#define positivo A0
#define ajustePin A7
#define negativo A2

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// macros
#define petenciometroVelocMax analogRead(ajustePin)
#define potenciometro5v digitalWrite(positivo, HIGH)
#define potenciometroGND digitalWrite(negativo, LOW)

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// variáveis
int vermelho = 0;
int verde = 0;
int azul = 255;
int velocidade_varre = 0;
int comtador;
char seguimento;
int brilho = 255;
int velocidade_minima = 1;
int velocidade_maxima = 160;
unsigned long limpaDisplay = 8000;
int contagem = 0;
int leitura = 0;
int dado = 0;
int velocidade = 0;
unsigned long tempo = 0;
const unsigned long reinicioContagem = 500;

CRGB leds[NUM_LEDS];
SoftwareSerial mySerial(3, 2);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// prototipo Funções
void Unidade(int nun);
void Decodifica(int numero);
void Seguimento(bool multiplo, char s);
void contaTempo(int _tempo);
void Numero(int);
void Radar(void);
bool Manual(void);
void Envia(void);
void teste(void);
void CalculaVelocidade(int _leitura, int _reinicioContagem, int _contagem);
void corDoDisplay(int velocidade, int _tempo);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Confiruração
void setup() {
  pinMode(positivo, OUTPUT);
  pinMode(ajustePin, INPUT);
  pinMode(negativo, OUTPUT);

  potenciometro5v;
  potenciometroGND;

  FastLED.addLeds<WS2811, DATA_PIN>(leds, NUM_LEDS);
  FastLED.setBrightness(brilho);
  mySerial.begin(9600);
  Serial.begin(115200);
  Serial.println("Pronto");
  Decodifica(188);
  delay(500);
  vermelho = 0, verde = 0, azul = 0;
  FastLED.clear();
  Decodifica(0);


  //     for (int i = 0; i <120; i++) {
  //     FastLED.clear();
  //     Decodifica(i);
  //     Serial.println(i);
  //     delay(5);
  //   }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Loop Principal
void loop() {
  //vermelho = 255, verde = 0, azul = 0;
  //Seguimento(1, 'h');
  corDoDisplay(velocidade, tempo);
  Radar();
  contaTempo(tempo);
  if (tempo > limpaDisplay) {
    CalculaVelocidade(leitura, reinicioContagem, contagem);
  }
  //Serial.println(tempo);
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Funçoes
void Seguimento(int multiplo, char s) {
  int digito = 0;

  if (multiplo >= 1) digito = 21;
  switch (s) {

    case 'a':
      for (int i = 0; i < 3; i++) {
        leds[i + digito] = CRGB(vermelho, verde, azul);
        //Serial.print(i);
        FastLED.show();
        delay(velocidade_varre);
      }
      break;

    case 'b':
      for (int i = 3; i < 6; i++) {
        leds[i + digito] = CRGB(vermelho, verde, azul);
        //Serial.print(i);
        FastLED.show();
        delay(velocidade_varre);
      }
      break;

    case 'c':
      for (int i = 6; i < 9; i++) {
        leds[i + digito] = CRGB(vermelho, verde, azul);
        FastLED.show();
        //delay(velocidade_varre);
      }
      break;
    case 'd':
      for (int i = 9; i < 12; i++) {
        leds[i + digito] = CRGB(vermelho, verde, azul);
        FastLED.show();
        delay(velocidade_varre);
      }
      break;
    case 'e':
      for (int i = 12; i < 15; i++) {
        leds[i + digito] = CRGB(vermelho, verde, azul);
        FastLED.show();
        delay(velocidade_varre);
      }
      break;
    case 'f':
      for (int i = 15; i < 18; i++) {
        leds[i + digito] = CRGB(vermelho, verde, azul);
        FastLED.show();
        delay(velocidade_varre);
      }
      break;
    case 'g':
      for (int i = 18; i < 21; i++) {
        leds[i + digito] = CRGB(vermelho, verde, azul);
        FastLED.show();
        delay(velocidade_varre);
      }
      break;
    case 'h':
      for (int i = 42; i < 48; i++) {  //  for (int i = 42; i < 51; i++) {
        leds[i + digito] = CRGB(vermelho, verde, azul);
        FastLED.show();
        delay(velocidade_varre);
      }
      break;
  }
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//
void Decodifica(int numero) {
  int multiplo = 0;
  int varredura = 2;
  int centena = 0;
  if (numero > 99) {
    numero = numero - 100;
    centena = 1;
  }
  //Serial.println(numero);
  int dezena = numero / 10;
  int unidade = numero % 10;

  numero = unidade;

  for (int i = 0; i < (varredura + 1); i++) {
    //int digito = unidade;
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
        Seguimento(multiplo, 'f');
        Seguimento(multiplo, 'g');
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
    if (centena == 1) {
      Seguimento(multiplo, 'h');
      centena = 0;
    }
    if (dezena > 0) {
      multiplo = 1;
      numero = dezena;
    } else {
      multiplo = 0;
    }
  }
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////

void Envia() {

  int value = 0;
  int loop_time = 87;

  // escreve o resultado
  if (Serial.availableForWrite()) {
    String outstr = String(String(leitura, DEC) + "," + String(loop_time, DEC) + "," + String(value, DEC));
    Serial.println(outstr);
    Serial.flush();
  }
}

/////////////////////////////////////////////////////////////////////////////////////////
void Radar(void) {

  while (mySerial.available() >= 12) {  // Verifica se há 12 bytes disponíveis
    byte dados[12];                     // Array para armazenar os dados recebidos
    mySerial.readBytes(dados, 12);      // Lê 12 bytes da porta serial
  
    if (dados[1] == 85) {
      for (int i = 0; i < 12; i++) {
        dado = dados[i];  // Converte o byte para inteiro
        //Serial.println(dado);
        if (i == 6) {  // Imprime o sexto elemento do array
          leitura = dado;
          //vermelho = 255, verde = 0, azul = 0;
          if ((leitura > velocidade_minima) && (leitura < velocidade_maxima)) {
            contagem++;
            //vermelho = 255, verde = 0, azul = 0;
            CalculaVelocidade(leitura, reinicioContagem, contagem);
          }
        }
      }
    }
    //Serial.println("");
  }
}

/////////////////////////////////////////////////////////////////////////////////////////
void CalculaVelocidade(int _leitura, int _reinicioContagem, int _contagem) {
  static int velocidades[3];
  static int passo = 0;
  static int ultimaLeitura = 0;
  int difetencaVelocidades = 10;
  //Serial.println(contagem);
  if (contagem) {
    switch (passo) {
      case 0:
        velocidades[0] = leitura;
        ultimaLeitura = leitura;
        //Serial.println(leitura);
        passo = 1;
        break;
      case 1:
        if (contagem > 1) {
          velocidades[1] = leitura;
          //Serial.println(velocidade);
          if ((velocidades[1] <= (velocidades[0] + difetencaVelocidades))
              && (velocidades[1] >= (velocidades[0] - difetencaVelocidades))) {
            velocidade = (velocidades[0] + velocidades[1]) / 2;
            Serial.println(velocidade);
            Decodifica(velocidade);
            tempo = 0;
            passo = 2;
          } else {
            tempo = 0;
            passo = 2;
            Serial.println("divergente");
          }
        }
        break;
      case 2:
        //Serial.println(tempo);
        if (tempo > reinicioContagem) {
          tempo = 0;
          passo = 0;
          contagem = 0;
          velocidade = 0;
          velocidades[0] = 0;
          velocidades[1] = 0;
          velocidades[2] = 0;
          velocidades[3] = 0;
          //Decodifica(0);
          //vermelho = 0, verde = 0, azul = 0;
          //CRGB(azul, verde, vermelho);
          vermelho = 0, verde = 0, azul = 0;
          FastLED.clear();
          Decodifica(0);
          Serial.println("aguardando");
        }
        break;
    }
  }
}
/////////////////////////////////////////////////////////////////////////////////////////
void corDoDisplay(int velocidade, int _tempo) {
  int velociDefinida = 0;
  int VelocMax = 150;
  static int ultimaVelociDefinida = 0;
  static int flag = 0;
  const int tolerancia = 50;
  const int tempoPersistencia = 10;


  velociDefinida = map(petenciometroVelocMax, 0, 1023, 0, VelocMax);
  velociDefinida = round(velociDefinida / 5) * 5;

  if ((flag > 0) && (tempo > tempoPersistencia)) {
    Serial.println("normal");
    FastLED.clear();
    velocidade = 0;
    vermelho = 0, verde = 0, azul = 0;
    CRGB(vermelho, verde, azul);
    FastLED.show();
    flag = 0;
    FastLED.clear();
  }

  if ((flag == 1) || (velociDefinida != ultimaVelociDefinida)) {
    velociDefinida = map(petenciometroVelocMax, 0, 1023, 0, VelocMax);
    velociDefinida = round(velociDefinida / 5) * 5;
    vermelho = 0, verde = 255, azul = 0;
    FastLED.show();
    FastLED.clearData();

    Decodifica(velociDefinida);
    Serial.println(velociDefinida);
    FastLED.show();
  }
  if ((flag == 0) && (velociDefinida != ultimaVelociDefinida)) {
    tempo = 0;
    flag = 1;
    ultimaVelociDefinida = velociDefinida;
    //vermelho = 255, verde = 0, azul = 0;
    Serial.println("nova velocidade");
    Serial.println(velociDefinida);
    vermelho = 0, verde = 255, azul = 0;
    CRGB(vermelho, verde, azul);
    Decodifica(velociDefinida);
    FastLED.show();
  }



  ultimaVelociDefinida = velociDefinida;

  if (velociDefinida <= velocidade) {
     vermelho = 0, verde = 255, azul = 0;
        //Serial.println("vermelho");
  } else {
    vermelho = 255, verde = 255, azul = 255;
   // Serial.println("verde");
  }
}
/////////////////////////////////////////////////////////////////////////////////////////
void contaTempo(int _tempo) {
  static unsigned long lastTime1 = 0;
  unsigned long currentTime = millis();  // guarda o tempo atual

  if ((currentTime - lastTime1) >= 1) {
    lastTime1 = currentTime;
    tempo++;
  }
}
