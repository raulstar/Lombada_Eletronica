

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// mapeamento de hardware
#define positivo A0
#define ajustePin A1
#define negativo A2

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// macros
#define petenciometroVelocMax analogRead(ajustePin)
#define potenciometro5v digitalWrite(positivo, HIGH)
#define potenciometroGND digitalWrite(negativo, LOW)

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// variáveis
int vermelho = 0, verde = 0, azul = 255;
int velocidade = 0;
long tempo = 0;

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// prototipo Funções
void corDoDisplay(int velocidade, int _tempo);
void contaTempo(int tempo);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Confiruração
void setup() {
  pinMode(positivo, OUTPUT);
  pinMode(ajustePin, INPUT);
  pinMode(negativo, OUTPUT);

  potenciometro5v;
  potenciometroGND;

  Serial.begin(9600);
  Serial.println("corDoDisplay");
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Loop Principal
void loop() {
  velocidade = 30;
  corDoDisplay(velocidade, tempo);
  contaTempo(tempo);
  delay(10);
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Funçoes
void corDoDisplay(int velocidade, int _tempo) {
  int velociDefinida = 0;
  int VelocMax = 150;
  static int ultimaVelociDefinida = 0;
  static int flag = 0;
  const int tolerancia = 50;
  const int tempoPersistencia = 600;

  velociDefinida = map(petenciometroVelocMax, 0, 1023, 0, VelocMax);
  //Serial.println(velociDefinida);
  if ((flag == 0) && (velociDefinida != ultimaVelociDefinida)) {
    tempo = 0;
    flag = 1;
    vermelho = 255, verde = 0, azul = 0;
    Serial.println("nova velocidade");
    Serial.println(velociDefinida);
  }
  if ((flag == 1) || (velociDefinida != ultimaVelociDefinida)) {
    velociDefinida = map(petenciometroVelocMax, 0, 1023, 0, VelocMax);
    Serial.println(velociDefinida);
  }
  if ((flag > 0) && (tempo > tempoPersistencia)) {
    Serial.println("normal");
    flag = 0;
  }

  ultimaVelociDefinida = velociDefinida;

  if (velociDefinida > velocidade) {
    vermelho = 255, verde = 0, azul = 0;
  } else {
    vermelho = 0, verde = 0, azul = 255;
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
/////////////////////////////////////////////////////////////////////////////////////////