#define leituras Serial.println(leitura)
#define velocidades1 Serial.println(velocidade)
#include <SoftwareSerial.h>

SoftwareSerial mySerial(2, 3);  // RX, TX  (ajuste conforme seu hardware)

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// variáveis
int contagem = 0;
int leitura = 0;
int velocidade = 0;
unsigned long tempo = 0;
const unsigned long reinicioContagem = 500;
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// prototipo Funções
void CalculaVelocidade(int _leitura, int _reinicioContagem, int _contagem);
void contaTempo(int _tempo);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Confiruração
void setup() {
  mySerial.begin(9600);
  Serial.begin(9600);
  Serial.println("leitura");
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Loop Principal
void loop() {
  contaTempo(tempo);
  if (velocidade) Serial.println(velocidade);
  int temp;
  if (mySerial.available()) {
    contagem++;
    leitura = (mySerial.read());
    //Serial.write(velocidade);
    CalculaVelocidade(leitura, reinicioContagem, contagem);
  }
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Funçoes
void CalculaVelocidade(int _leitura, int _reinicioContagem, int _contagem) {
  static int velocidades[3];
  static int passo = 0;
  static int ultimaLeitura = 0;
  int difetencaVelocidades = 10;
  //Serial.println(leitura);
  if (contagem) {
    switch (passo) {
      case 0:
        velocidades[0] = leitura;
        ultimaLeitura = leitura;
        Serial.println(velocidade);
        passo = 1;
        break;
      case 1:
        if (contagem == 2) {
          velocidades[1] = leitura;
          if ((velocidades[1] <= (velocidades[0] + difetencaVelocidades))
              && (velocidades[1] >= (velocidades[0] - difetencaVelocidades))) {
            velocidade = (velocidades[0] + velocidades[1]) / 2;
            //Serial.println(velocidade);
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
          Serial.println("aguardando");
        }
        break;
    }
  }
}

/////////////////////////////////////////////////////////////////////////////////////////
void contaTempo(int _tempo) {
  static unsigned long lastTime1 = 0;
  unsigned long currentTime = millis();  // guarda o tempo atual

  if ((currentTime - lastTime1) >= 1) {  // verifica se já passaram 500ms desde a última mudança
    lastTime1 = currentTime;
    tempo++;
  }
}