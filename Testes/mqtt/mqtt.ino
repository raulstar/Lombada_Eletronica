//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//             Pulsadores Tactil com Internet das Coisas: ESP32, IBM Watson e Node-Red com ESP32 Dev module
//                              Modulo master
//   build 08/09/2021 by Eng. Raul 
//  v2.0
//////////////////////////////////////////////////////////////////////////////////////////////////////////////

//============================================================================================================= */
// Link da pagina de controle:
//https://internetofthings.ibmcloud.com/
//https://autorobotica.mybluemix.net/ui/#!/0?socketid=UcajIY2IPIzD0mtiAADT
// Link NODERED
//https://autorobotica.mybluemix.net/red/#flow/544e9c75.42d854

//============================================================================================================= */
//Referencias:
//https://www.youtube.com/watch?v=9bN3aXjRbF4&ab_channel=FernandoKTecnologia
//https://www.youtube.com/watch?v=9ExcHytl4mg&t=672s&ab_channel=FernandoKTecnologia
//https://www.youtube.com/watch?v=cuSimO5e_fU&ab_channel=FernandoKTecnologia
//https://www.youtube.com/watch?v=FHuaBUSwlWc&list=PL7CjOZ3q8fMdecH0Ppxg6BloyXAFi6_-A&index=8&ab_channel=BrincandocomIdeiasBrincandocomIdeias
//https://www.youtube.com/watch?v=996cM16-urU&list=PL7CjOZ3q8fMdecH0Ppxg6BloyXAFi6_-A&index=7&ab_channel=BrincandocomIdeiasBrincandocomIdeias


// =============================================================================================================
// --- Bibliotecas Auxiliares ---
//https://flows.nodered.org/node/node-red-contrib-scx-ibmiotapp
//https://github.com/zhouhan0126/DNSServer---esp32
//https://github.com/zhouhan0126/WebServer-esp32
//https://github.com/zhouhan0126/WIFIMANAGER-ESP32

#include <Arduino.h>
#include <WiFi.h> 
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DNSServer.h>
#include <WebServer.h>
#include <WiFiManager.h>
#include "BluetoothSerial.h"

// =============================================================================================================
// --- Variáveis Globais para conecção bluetooth---

String MACadd = "4C:EB:D6:74:C9:0A";// "A4:E5:7C:47:10:CA" "4C:EB:D6:74:C9:0A"Endereço do Bluetooth
uint8_t address[6] = {0x4C, 0xEB, 0xD6, 0x74, 0xC9, 0x0A};// {0xA4, 0xE5, 0x7C, 0x47, 0x10, 0xCA};{0x4C, 0xEB, 0xD6, 0x74, 0xC9, 0x0A}
String name = "Pulsador";
char *pin = "1234"; //<- standard pin would be provided by default
bool connected;

// =============================================================================================================
// --- Variáveis Globais para conecção com o IBM Ilot ---
//---//https://internetofthings.ibmcloud.com/
// Altere estes dados pelos obtidos ao cadastrar o novo dispopsitivo no IBM Watson Iot

const String ORG = "xo3jx7"; //ID  da organização no IBM Watson
const String DEVICE_TYPE = "ESP32";
const String DEVICE_ID = "PULSADOR"; //ID DO DISPOSITIVO
#define DEVICE_TOKEN "0123456789"

// =============================================================================================================
// DEFINIÇÕES DE PINOS
#define vibrador 17
#define led 16
#define ledOnBord 02 //led para mostrar conexão
#define botaoDesliga 15
#define botaoLiga GPIO_NUM_4
// =============================================================================================================
// FORMADO DAS MENSAGENS PARA MQTT

const char eventTopic[] = "iot-2/evt/status/fmt/json";
const String CLIENT_ID = "d:" + ORG + ":" + DEVICE_TYPE + ":" + DEVICE_ID; //Constantes para conexão do servidor mqtt
const String MQTT_SERVER = ORG + ".messaging.internetofthings.ibmcloud.com";

#define COMMAND_TOPIC_R1 "iot-2/cmd/commandR1/fmt/json"
#define COMMAND_TOPIC_R2 "iot-2/cmd/commandR2/fmt/json"
#define COMMAND_TOPIC_R3 "iot-2/cmd/commandR3/fmt/json"
#define COMMAND_TOPIC_R4 "iot-2/cmd/commandR4/fmt/json"
#define COMMAND_TOPIC_R5 "iot-2/cmd/commandR5/fmt/json"

// =============================================================================================================
// variáveis globais

int cont = 0;
int liga;
int alterna;
long intensidade = 100;
int duracao;
int inicia;
const int ledPin = 05;
String comando = "";
char valorRecebido;
bool comectado;

//int botaoDesliga = 15; //pino para dormir

// =============================================================================================================
// objetos para conexão do servidor mqtt


BluetoothSerial SerialBT;
hw_timer_t * timer = NULL;

void Desliga(){
    liga = 0;
    Serial.println("Desligando");
    SerialBT.write('d');
    digitalWrite(ledOnBord, LOW);
    digitalWrite(vibrador, LOW);
    digitalWrite(led, LOW);
    timerEnd(timer);
    timer = NULL; 
    esp_deep_sleep_start();
    
}

void cb_timer(){
  static bool estado = 0;
  if(digitalRead(botaoDesliga)==0)  Desliga();
  if (estado == LOW) {
    digitalWrite(led, estado);
    estado = HIGH;
  }
  else {
    digitalWrite(led, estado);
    estado = LOW;
  }
      
      
    static unsigned int counter = 1;
    /* Serial.println("cb_timer(): ");
    Serial.print(counter);
    Serial.print(": ");
    Serial.print(millis()/1000);
    Serial.println(" segundos"); */
    if(comectado) digitalWrite(led, HIGH);
    else  digitalWrite(led, estado);
    // if the led is off turn it on and vice-versa:
      
    // set the led with the estado of the variable:
    digitalWrite(ledOnBord, estado);

}

void startTimer(){
  
    //inicialização do timer. Parametros:
    /* 0 - seleção do timer a ser usado, de 0 a 3.
      80 - prescaler. O clock principal do ESP32 é 80MHz. Dividimos por 80 para ter 1us por tick.
    true - true para contador progressivo, false para regressivo
    */
    timer = timerBegin(0, 80, true);

    /*conecta à interrupção do timer
     - timer é a instância do hw_timer
     - endereço da função a ser chamada pelo timer
     - edge=true gera uma interrupção
    */
    timerAttachInterrupt(timer, &cb_timer, true);

    /* - o timer instanciado no inicio
       - o valor em us para 1s
       - auto-reload. true para repetir o alarme
    */
    timerAlarmWrite(timer, 1000000, true); 

    //ativa o alarme
    timerAlarmEnable(timer);
    
}

// =============================================================================================================
// CONFIGURAÇÃO

void setup()
{
    esp_sleep_enable_ext0_wakeup(botaoLiga,0); //pino para acordar 1 = High, 0 = Low

    Serial.begin(9600); //velocidade de comunicação serial
    
    Serial.println("Pulsadores Tactil com Internet das Coisas: ESP32, IBM Watson e Node-Red...");
    Serial.println("Versão 2.00");
    Serial.println("Raul Engenharia");
    SerialBT.setPin(pin); //pino bluetooth on board
    Serial.println("bluetooth onboard habilitado");
    SerialBT.begin("ESP32", true); //habilita o bluetooth é um board
    Serial.println("verifique se o bluetooth do outro dispositivo está ligado!");

        //configuração dos pinos de entrada e saída
    pinMode(vibrador, OUTPUT);
    pinMode(led, OUTPUT);
    pinMode(ledOnBord, OUTPUT);
    digitalWrite(ledOnBord, LOW);
    //pinMode (botaoDesliga, INPUT);
    pinMode(botaoDesliga, INPUT_PULLUP);
    //pinMode (botaoLiga, INPUT);
    pinMode(botaoLiga, INPUT_PULLUP);

    //testes das portas
    digitalWrite(vibrador, HIGH);
    digitalWrite(led, HIGH);
    delay(1500);
    digitalWrite(vibrador, LOW);
    //digitalWrite(led, LOW);

    Serial.println("");
    Serial.println("EMDR Pulsadores Tactil Iot");
    Serial.println("Modulo master");
    Serial.println("Dados para conexão com outro dispositivo bluetooth");
    Serial.println(" MACadd = 98:D3:31:40:14:57"); //Endereço do Bluetooth
    Serial.println(" address[6]  = {0x98, 0xD3, 0x31, 0x40, 0x14, 0x57}");
    Serial.println(" name = HC-05");
    Serial.println(" pin = 1234");

    Serial.println("");
    Serial.println("dados da cloud da ibm usando o ibm watson");
    Serial.println(" ORG = ld48yg"); //ID  da organização no IBM Watson
    Serial.println(" DEVICE_TYPE = ESP32");
    Serial.println(" DEVICE_ID = test3"); //ID DO DISPOSITIVO
    Serial.println(" DEVICE_TOKEN 0123456789");

    connected = SerialBT.connect(address);

    //startTimer();

    if (connected)
    {
        SerialBT.write('c');
        Serial.println("Bluetooth conectado!");
    }
    else
    {
        int static temp;
        while ((!SerialBT.connected(1000)) && (temp < 2))
        { 
            temp++;
            Serial.println("falha ao conectar ao Bluetooth");
        }
    }

    //Página de conexão da rede Wi-Fi
    WiFiManager wifiManager;
    wifiManager.setAPCallback(configModeCallback);
    wifiManager.setSaveConfigCallback(saveConfigCallback);
    wifiManager.autoConnect("Autoraf"); //Nome da janela da configuração da rede Wi-Fi

    connectMQTTServer(); //conexão com servidor mqtt
   
}

WiFiClient wifiClient;
PubSubClient client(MQTT_SERVER.c_str(), 1883, wifiClient);
// =============================================================================================================
// LOOP PRINCIPAL

void loop()
{
    digitalWrite(led, HIGH);
    valorRecebido =(char)SerialBT.read();

    client.loop(); //Verificação das mensagens que chegam do mqtt
    atualiza();
    if (Serial.available())
    {
        SerialBT.write(Serial.read());
    }
    
    if (SerialBT.available())
    {
        Serial.write(SerialBT.read());
    }
    delay(20);
    if(liga){
  digitalWrite(vibrador, HIGH);
  if(!alterna)SerialBT.write('M');
    if(alterna)SerialBT.write('m');
  delay(intensidade);
  digitalWrite(vibrador, LOW);
  if(!alterna)SerialBT.write('m');
    if(alterna)SerialBT.write('M');
  if(!liga)SerialBT.write('d');
  delay(intensidade);
  }
    

    // if (liga)//comandos recebidos por bluetooth
    // {
    //     digitalWrite(vibrador, HIGH);
    //     if (!alterna)  {
    //       SerialBT.write('M');
    //        Serial.write('M');
    //     }
    //     if (alterna) {
    //       SerialBT.write('m');
    //       Serial.write('m');
    //     }
    //     delay(intensidade);
    //     digitalWrite(vibrador, LOW);
    //     if (!alterna){
    //       SerialBT.write('m');
    //       Serial.write('m');
    //     }
    //     if (alterna) {
    //       SerialBT.write('M');
    //       Serial.write('M');
    //     }
    //     if (!liga) {
    //       SerialBT.write('d');
    //       Serial.write('d');
    //     //SerialBT.write('l');
    //     }
    //     delay(intensidade);
    // }
    // Aguarda 500 milissegundos
    if(digitalRead(botaoDesliga)==0)  Desliga();
    
}

// =============================================================================================================
//
//Função responsável pela conexão ao servidor MQTT

void connectMQTTServer()
{
    Serial.println("Conectando ao servidor MQTT...");

    if (client.connect(CLIENT_ID.c_str(), "use-token-auth", DEVICE_TOKEN))
    { //Verifique essa conexão foi estabelecida com o servidor mqtt
        Serial.println("Conectado ao Broker MQTT...");
         digitalWrite(led, HIGH);
        client.setCallback(callback);
        //Inscrição nos tópicos do servidor mqtt
        client.subscribe(COMMAND_TOPIC_R1);
        client.subscribe(COMMAND_TOPIC_R2);
        client.subscribe(COMMAND_TOPIC_R3);
        client.subscribe(COMMAND_TOPIC_R4);
        client.subscribe(COMMAND_TOPIC_R5);
        digitalWrite(ledOnBord, HIGH); //ledOnBord indicando que a conexão foi feita com sucesso  
        comectado = 1;      
    }
    else
    {
        Serial.print("erro = ");
        Serial.println(client.state());
        connectMQTTServer();
        comectado = 0;  
        atualiza(); 

    }
}

// =============================================================================================================
// Função executada quando chegar algum pacote do servidor mqtt

void callback(char *topic, unsigned char *payload, unsigned int length)
{
    //Implementação de objetos para extrair as valor do pacote recebido
   // StaticJsonBuffer<30> jsonBuffer;
    JsonObject &root = jsonBuffer.parseObject(payload);

    if (!root.success())
    {
        Serial.println("Erro no Json Parse");
        return;
    }

    int value = root["value"]; //valor extraído do pacote
                               //  char convert = char *topic[18];

    Serial.println("recebendo...");
    //verifica se o tópico que chegou é o correspondente abaixo
    if (strcmp(topic, COMMAND_TOPIC_R1) == 0)
    {
        liga = value;
        if (value)
        {
            digitalWrite(vibrador, value);
            Serial.print("Ligado ");
            Serial.println(value);
        }
        if (!value)
        {
            alterna = value;            
            digitalWrite(vibrador, value);
            Serial.print("Desligado ");
            Serial.println(value);
            
        }
    }
    if (strcmp(topic, COMMAND_TOPIC_R2) == 0)
    {
        if (value)
        {
            inicia = value;
            Serial.print("Inicia ");
            Serial.println(value);
        }
        if (!value)
        {
            inicia = value;
            Serial.print("Para ");
            Serial.println(value);
        }
    }
    if (strcmp(topic, COMMAND_TOPIC_R3) == 0)
    {
        alterna = value;
        Serial.println("alternando ");
        Serial.println(value);
    }
    if (strcmp(topic, COMMAND_TOPIC_R4) == 0)
    {
        digitalWrite(led, value);
        Serial.println("acionando R4 ");
        Serial.println(value);
    }
    if (strcmp(topic, COMMAND_TOPIC_R5) == 0)
    {
        if ((value) && (intensidade < 5000))
            intensidade = intensidade + 100;
        if ((value == 0) && (intensidade != 0))
            intensidade = intensidade - 100;

        String payload = "{\"d\":{\"adc\":"; // Inicia uma String associando ao endereço
        payload += intensidade;              // Atribui o valor de leitura de cont a String
        payload += "}}";                     // Finaliza a String
        Serial.print("Enviando payload: ");
        Serial.println(payload);                             // Escreve a String no monitor Serial
        client.publish(eventTopic, (char *)payload.c_str()); // Publica a String
        Serial.println("intensidade");
        Serial.println(value);
        Serial.println(intensidade);
    }
}

// =============================================================================================================
// o objeto da página de configuração da rede wi fi

void configModeCallback(WiFiManager *myWiFiManager)
{
    Serial.println("Entrou no modo de configuração");
    Serial.println(WiFi.softAPIP());
    Serial.println(myWiFiManager->getConfigPortalSSID());
}

// =============================================================================================================
// salva a configuração da rede wi fi

void saveConfigCallback()
{
    Serial.println("Configuração salva");
    Serial.println("Reinicie o pulsador");
    Serial.println(WiFi.softAPIP());
}

int atualiza() {
  unsigned long tempoAtual = millis();
  static bool estado = 0;
  static unsigned long tempoPrevio = 0;        // will store last time led was updated
  static const long interval = 1000;         // constants won't change:
  
  if (tempoAtual - tempoPrevio >= interval) {
    // save the last time you blinked the led
    tempoPrevio = tempoAtual;
            
    if(comectado) digitalWrite(led, HIGH);
    else  digitalWrite(led, estado);
    // if the led is off turn it on and vice-versa:
    if (estado == LOW) {
      estado = HIGH;
      Serial.print(".");

      if (SerialBT.available())
   {
       char valorRecebido;
       valorRecebido =(char)SerialBT.read();
       
       if (valorRecebido == 'c'){ String payload = "{\"c\":{\"adc\":";
       Serial.print("Enviando payload: ");
       Serial.println(payload);  
       client.publish(eventTopic, (char *)payload.c_str());
       }
   }
   else{
      String payload = "{\"b\":{\"adc\":"; // Inicia uma String associando ao endereço
        payload += "1";              // Atribui o valor de leitura de cont a String
        payload += "}}";                     // Finaliza a String
        Serial.print("Enviando payload: ");
        Serial.println(payload);                             // Escreve a String no monitor Serial
        client.publish(eventTopic, (char *)payload.c_str()); // Publica a String
        Serial.println("CONECTADO");
    }
      return 1;
    } else {
      estado = LOW;
      return 0;
    }

    // set the led with the estado of the variable:
    digitalWrite(ledOnBord, estado);
  }
}