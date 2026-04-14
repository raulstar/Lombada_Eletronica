/*
  Sorteador de números (5 a 20) — diferença < 10
  ----------------------------------------------
  • Envia cada número pela Serial (9600 baud).
  • Entre sorteios, espera 400 ms – 1000 ms (aleatório).
  • A diferença |atual – anterior| é sempre < 10.
*/

const int LIMITE_INFERIOR   = 5;
const int LIMITE_SUPERIOR   = 20;

const int MIN_INTERVALO_MS  = 400;   // 0,4 s
const int MAX_INTERVALO_MS  = 1000;  // 1,0 s

int numeroAnterior = -1;  // sentinel (−1 = primeira rodada)

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(A0));        // semente imprevisível
  Serial.println("Iniciando sorteios...\n");
}

void loop() {
  int numeroAtual;

  // Gera até que a diferença para o anterior seja < 10 (exceto na 1ª vez)
  do {
    numeroAtual = random(LIMITE_INFERIOR, LIMITE_SUPERIOR + 1);  // 5‑20 (20 incluído)
  } while (numeroAnterior != -1 && abs(numeroAtual - numeroAnterior) >= 10);

  // Exibe o resultado
  Serial.print("Número sorteado: ");
  Serial.println(numeroAtual);

  // Atualiza referência para a próxima verificação
  numeroAnterior = numeroAtual;

  // Espera um tempo aleatório de 400 ms a 1000 ms (1000 incluído)
  int intervalo = random(MIN_INTERVALO_MS, MAX_INTERVALO_MS + 1);
  delay(intervalo);
}
