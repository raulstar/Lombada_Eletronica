/*
 * Vetores de comprimento 1 a 6 com números aleatórios entre 6 e 20
 * Cada número é enviado individualmente, com atraso aleatório de 400 ms‑1 s
 */

const int MIN_RAND = 6;
const int MAX_RAND = 20;

const int MIN_RAND2 = 1;
const int MAX_RAND2 = 10;

const unsigned int MIN_DELAY_MS = 200;   // 400 ms
const unsigned int MAX_DELAY_MS = 800;  // 1 000 ms  (limite superior exclusivo → +1 no random())

int vetor1[1];
int vetor2[2];
int vetor3[3];
int vetor4[4];
int vetor5[5];
int vetor6[6];

void preencherVetores() {
  vetor1[0] = random(MIN_RAND, MAX_RAND + 1);

  for (int i = 0; i < 2; i++) vetor2[i] = random(MIN_RAND, MAX_RAND + 1);
    for (int i = 0; i < 1; i++) vetor2[i] =200;
  for (int i = 0; i < 3; i++) vetor3[i] = 0;
  for (int i = 0; i < ( random(MIN_RAND2, MAX_RAND2 + 1)); i++) vetor6[i] =0;
  for (int i = 0; i < 4; i++) vetor4[i] = 0;
  for (int i = 0; i < ( random(MIN_RAND2, MAX_RAND2 + 1)); i++) vetor6[i] =0;
  for (int i = 0; i < 5; i++) vetor5[i] = random(MIN_RAND, MAX_RAND + 1);
  for (int i = 0; i < ( random(MIN_RAND2, MAX_RAND2 + 1)); i++) vetor6[i] =0;
  for (int i = 0; i < 5; i++) vetor5[i] = random(MIN_RAND, MAX_RAND + 1);
}

void tratarNumero(int valor, int vetor, int indice) {
  // 1) Mostra no Serial
  // Serial.print("Vetor");
  // Serial.print(vetor);
  // Serial.print('[');
  // Serial.print(indice);
  // Serial.print("] = ");
  Serial.println(valor);

  // 2) Espera entre 400 ms e 1 s antes de enviar o próximo
  unsigned int espera = random(MIN_DELAY_MS, MAX_DELAY_MS + 1);
  delay(espera);
}

void processarVetores() {
  tratarNumero(vetor1[0], 1, 0);

  for (int i = 0; i < 2; i++) tratarNumero(vetor2[i], 2, i);
  for (int i = 0; i < 3; i++) tratarNumero(vetor3[i], 3, i);
  for (int i = 0; i < 4; i++) tratarNumero(vetor4[i], 4, i);
  for (int i = 0; i < 5; i++) tratarNumero(vetor5[i], 5, i);
  for (int i = 0; i < 6; i++) tratarNumero(vetor6[i], 6, i);

  Serial.println();  // linha em branco para separar lotes
}

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(A0));  // semente p/ números aleatórios

  preencherVetores();
  processarVetores();
}

void loop() {
  // Gera um novo lote a cada 5 s (só para demonstração; ajuste se quiser)
  static unsigned long ultimaExecucao = 0;
  if (millis() - ultimaExecucao > 5000) {
    preencherVetores();
    processarVetores();
    ultimaExecucao = millis();
  }
}
