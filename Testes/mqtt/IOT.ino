//////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                           Pulsadores Tactil com Internet das Coisas: ESP32, IBM Watson e Node-Red
//
//   build 08/09/2021 by Raul and Pooja
//  v2.0
//////////////////////////////////////////////////////////////////////////////////////////////////////////////

//============================================================================================================= */
// Link da pagina de controle:
//https://autoraf-2.mybluemix.net/ui/#!/1?socketid=dZq8Ij2y-cI3iEI8AAAB
//https://autorobotica.mybluemix.net/ui/#!/0?socketid=UcajIY2IPIzD0mtiAADT
// Link NODERED
//https://autorobotica.mybluemix.net/red/#flow/544e9c75.42d854
//https://autoraf-2.mybluemix.net/

//============================================================================================================= */
//Referencias:
//https://www.youtube.com/watch?v=9bN3aXjRbF4&ab_channel=FernandoKTecnologia
//https://www.youtube.com/watch?v=9ExcHytl4mg&t=672s&ab_channel=FernandoKTecnologia
//https://www.youtube.com/watch?v=cuSimO5e_fU&ab_channel=FernandoKTecnologia
//https://www.youtube.com/watch?v=FHuaBUSwlWc&list=PL7CjOZ3q8fMdecH0Ppxg6BloyXAFi6_-A&index=8&ab_channel=BrincandocomIdeiasBrincandocomIdeias
//https://www.youtube.com/watch?v=996cM16-urU&list=PL7CjOZ3q8fMdecH0Ppxg6BloyXAFi6_-A&index=7&ab_channel=BrincandocomIdeiasBrincandocomIdeias
//https://internetofthings.ibmcloud.com/

// =============================================================================================================
// --- Bibliotecas Auxiliares ---
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

// =============================================================================================================
// --- Variáveis Globais para conecção bluetooth---

// =============================================================================================================
// --- Variáveis Globais para conecção com o IBM Ilot ---
//---//https://internetofthings.ibmcloud.com/
// Altere estes dados pelos obtidos ao cadastrar o novo dispopsitivo no IBM Watson Iot

const String ORG = "ld48yg"; //ID  da organização no IBM Watson
const String DEVICE_TYPE = "ESP32";
const String DEVICE_ID = "test3"; //ID DO DISPOSITIVO
#define DEVICE_TOKEN "0123456789"

// =============================================================================================================
// DEFINIÇÕES DE PINOS
#define vibrador 05
#define pinRele2 04
#define pinLED 02 //LED para mostrar conexão

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

// =============================================================================================================
// objetos para conexão do servidor mqtt

WiFiClient wifiClient;
PubSubClient client(MQTT_SERVER.c_str(), 1883, wifiClient);

// =============================================================================================================
// CONFIGURAÇÃO

void setup()
{

    Serial.begin(9600); //velocidade de comunicação serial
    Serial.println("Pulsadores Tactil com Internet das Coisas: ESP32, IBM Watson e Node-Red...");
    Serial.println("verifique se o bluetooth do alto dispositivo está ligado!");

    //configuração dos pinos de entrada e saída
    pinMode(vibrador, OUTPUT);
    pinMode(pinRele2, OUTPUT);
    pinMode(pinLED, OUTPUT);
    digitalWrite(pinLED, LOW);

    Serial.println("");
    Serial.println("dados da cloud da ibm usando o ibm watson");
    Serial.println(" ORG = ld48yg"); //ID  da organização no IBM Watson
    Serial.println(" DEVICE_TYPE = ESP32");
    Serial.println(" DEVICE_ID = test3"); //ID DO DISPOSITIVO
    Serial.println(" DEVICE_TOKEN 0123456789");

    //Página de conexão da rede Wi-Fi
    WiFiManager wifiManager;
    wifiManager.setAPCallback(configModeCallback);
    wifiManager.setSaveConfigCallback(saveConfigCallback);
    wifiManager.autoConnect("Autoraf"); //Nome da janela da configuração da rede Wi-Fi

    connectMQTTServer(); //conexão com servidor mqtt
}

// =============================================================================================================
// LOOP PRINCIPAL

void loop()
{

    client.loop(); //Verificação das mensagens que chegam do mqtt

    delay(20);

    if (liga)
    {

    }
    // Aguarda 500 milissegundos
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
        client.setCallback(callback);
        //Inscrição nos tópicos do servidor mqtt
        client.subscribe(COMMAND_TOPIC_R1);
        client.subscribe(COMMAND_TOPIC_R2);
        client.subscribe(COMMAND_TOPIC_R3);
        client.subscribe(COMMAND_TOPIC_R4);
        client.subscribe(COMMAND_TOPIC_R5);
        digitalWrite(pinLED, HIGH); //Led indicando que a conexão foi feita com sucesso
    }
    else
    {
        Serial.print("erro = ");
        Serial.println(client.state());
        connectMQTTServer();
    }
}

// =============================================================================================================
// Função executada quando chegar algum pacote do servidor mqtt

void callback(char *topic, unsigned char *payload, unsigned int length)
{
    //Implementação de objetos para extrair as valor do pacote recebido
 //   StaticJsonBuffer<30> jsonBuffer;
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
        digitalWrite(pinRele2, value);
        Serial.println("acionando R4 ");
        Serial.println(value);
    }
    if (strcmp(topic, COMMAND_TOPIC_R5) == 0)
    {
        if ((value) && (intensidade < 5000))
            intensidade = intensidade + 100;
        if ((value == 0) && (intensidade != 0))
            intensidade = intensidade - 100;

        String payload = "{\"b\":{\"adc\":"; // Inicia uma String associando ao endereço
        payload += intensidade;              // Atribui o valor de leitura de cont a String
        payload += "}}";                     // Finaliza a String
        Serial.print("Enviando payload: ");
        Serial.println(payload);                             // Escreve a String no monitor Serial
        client.publish(eventTopic, (char *)payload.c_str()); // Publica a String
        Serial.println("acionando R5");
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
    Serial.println(WiFi.softAPIP());
}
