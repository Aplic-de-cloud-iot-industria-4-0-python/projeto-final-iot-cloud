# Automação Residencial para Preparo de Café Inteligente

O projeto de Automação Residencial para Preparo de Café Inteligente é uma solução inovadora que integra tecnologias de Internet das Coisas (IoT) e sensores ambientais para oferecer uma experiência automatizada e eficiente na preparação do café. Utilizando componentes eletrônicos avançados e conectividade com a nuvem, o sistema garante a qualidade do café e se adapta às condições ambientais.
## Componentes Principais: 
- **Arduino GIGA R1 WiFi:**  O cérebro do sistema, responsável pelo controle e integração de todos os componentes. 
- **Sensor de Temperatura e Umidade (DHT11):**  Monitora o ambiente e fornece dados em tempo real sobre as condições de temperatura e umidade. 
- **Sensor de Nível de Água:**  Mede o nível de água na cafeteira para garantir que haja água suficiente para preparar o café. 
- **Display LCD (I2C):**  Exibe informações relevantes, como temperatura, umidade, nível de água e status do sistema. 
- **Relé:**  Controla o funcionamento da cafeteira, permitindo ligá-la e desligá-la remotamente. 
- **LED Indicador:**  Fornece feedback visual sobre o status do sistema, como quando a temperatura limite é atingida. 
- **WiFi e MQTT:**  Para comunicação e controle remoto via internet.
## Funcionalidades Principais: 
- **Controle Remoto da Cafeteira:**  Os usuários podem ligar e desligar a cafeteira remotamente através de um aplicativo ou interface web. 
- **Monitoramento Ambiental:**  O sistema monitora constantemente a temperatura e umidade do ambiente, garantindo condições ideais para o preparo do café. 
- **Medição do Nível de Água:**  O sensor de água verifica se há água suficiente na cafeteira e exibe essa informação no LCD. 
- **Agendamento Automático:**  A cafeteira pode ser programada para ligar automaticamente em horários específicos, como pela manhã às 07:00, para garantir que o café esteja pronto quando os usuários acordarem. 
- **Feedback Visual e de Status:**  LEDs indicadores fornecem feedback visual sobre o estado do sistema, como alertas de temperatura máxima atingida. 
- **Exibição de Informações:**  O display LCD mostra as leituras atuais de temperatura, umidade, nível de água e status da cafeteira. 
- **Notificações via MQTT:**  Envia informações sobre temperatura, umidade e nível de água para a nuvem, permitindo monitoramento remoto.
## Integração com IoT na Nuvem: 
- **Coleta e Envio de Dados:**  Todas as informações coletadas pelo sistema são enviadas para uma plataforma de IoT na nuvem para armazenamento, análise e monitoramento remoto. 
- **Acesso Remoto:**  Os usuários podem acessar o status do sistema e receber notificações em tempo real sobre eventos importantes, como falhas no sistema ou cafeteira pronta. 
- **Controle Remoto:**  Através do protocolo MQTT, o sistema permite controle remoto eficiente e em tempo real.
## Benefícios: 
- **Conveniência:**  Os usuários podem preparar café automaticamente e programar o sistema de acordo com suas preferências. 
- **Eficiência Energética:**  A cafeteira só é acionada quando as condições ambientais são ideais, economizando energia. 
- **Controle Remoto:**  Os usuários têm controle total sobre o sistema, podendo monitorar e controlar remotamente a cafeteira. 
- **Personalização:**  O sistema pode ser personalizado para atender às preferências individuais dos usuários, garantindo uma experiência de café sob medida.
## Protocolos de Comunicação: 
- **MQTT (Message Queuing Telemetry Transport):**  
- **Descrição:**  Um protocolo leve de mensagens baseado em TCP/IP, ideal para comunicação entre dispositivos IoT devido à sua baixa sobrecarga e eficiência em redes com largura de banda limitada. 
- **Aplicação:**  Usado para enviar dados de sensores, status do sistema e comandos de controle entre o dispositivo Arduino e a plataforma de IoT na nuvem. Suporta publicação/assinatura de tópicos, permitindo comunicação assíncrona entre dispositivos e a nuvem. 
- **HTTP (Hypertext Transfer Protocol):**  
- **Descrição:**  Um protocolo de comunicação amplamente utilizado na web para transferência de dados entre clientes e servidores. 
- **Aplicação:**  Pode ser utilizado para comunicação entre o dispositivo Arduino e a nuvem através de requisições GET, POST e PUT, enviando e recebendo dados JSON. Ideal para ambientes onde a compatibilidade com a infraestrutura web existente é importante. 
- **CoAP (Constrained Application Protocol):**  
- **Descrição:**  Um protocolo de aplicação da Internet projetado para dispositivos com restrições de recursos, como dispositivos IoT. 
- **Aplicação:**  Permite comunicação eficiente e assíncrona entre dispositivos em redes com restrições de largura de banda e energia. Pode ser uma opção adequada para ambientes onde a eficiência de recursos é uma prioridade. 
- **WebSockets:**  
- **Descrição:**  Um protocolo de comunicação bidirecional, full-duplex, baseado em TCP, que permite a comunicação interativa em tempo real entre clientes e servidores. 
- **Aplicação:**  Pode ser utilizado para estabelecer uma conexão persistente entre o dispositivo Arduino e a nuvem, permitindo a transmissão contínua de dados e notificações em tempo real.

## Código

```cpp
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "DHT.h"
#include <WiFi.h>
#include <PubSubClient.h>

// Parametros de conexão WiFi e MQTT
const char* ssid = "Penelopecharmosa"; // REDE
const char* password = "13275274"; // SENHA

const char* mqtt_broker = "b37.mqtt.one"; // Host do broker
const char* topic = "2bqsvw6678/"; // Tópico a ser subscrito e publicado
const char* mqtt_username = "2bqsvw6678"; // Usuário
const char* mqtt_password = "0efiqruwxy"; // Senha
const int mqtt_port = 1883; // Porta

// MQTT Broker com MQTTBox e NQTTX com mosquitto -> Conectado
// const char *mqtt_broker = "test.mosquitto.org";  // Host do broker
// const char *topic = "grupo5/cafeteira";            // Tópico a ser subscrito e publicado
// const char *mqtt_username = "";                 // Usuário
// const char *mqtt_password = "";                 // Senha
// const int mqtt_port = 1883;                     // Porta

// MQTTX
// const char *mqtt_broker = "broker.emqx.io";  // Host do broker
// const char *topic = "grupo5/cafeteira";            // Tópico a ser subscrito e publicado
// const char *mqtt_username = "2bqsvw6678";                 // Usuário
// const char *mqtt_password = "0efiqruwxy";                 // Senha
// // const char *client_id = "mqttx_80be1b8f";                 // Senha
// const int mqtt_port = 8083;                     // Porta

// // iotbind -> Utilizar o app do IoTBind
// const char *mqtt_broker = "b37.mqtt.one";  // Host do broker
// const char *topic = "45eiqx7836";            // Tópico a ser subscrito e publicado
// const char *mqtt_username = "45eiqx7836";                 // Usuário
// const char *mqtt_password = "357fgiuwyz";                 // Senha
// const int mqtt_port = 1883;                     // Porta

// // myqtthub -> Utilizar o app do IoTBind
// const char *mqtt_broker = "node02.myqtthub.com";  // Host do broker
// const char *topic = "grupo5/myqtthub";            // Tópico a ser subscrito e publicado
// const char *mqtt_username = "estevam5s";                 // Usuário
// const char *mqtt_password = "PX7ppiJ7-VBtBdAfH";                 // Senha
// const char *client_id = "estevamsouzalaureth@gmail.com";                 // Senha
// const int mqtt_port = 8883;                     // Porta

// Pino do relé
const int relayPin = 52; // Use o pino correto para o relé

// DHT sensor
#define DHTTYPE DHT11 // DHT 11
#define dht_dpin 0 // Pino de dados do DHT11
DHT dht(dht_dpin, DHTTYPE); 
int LED = 7; // Ajuste o pino LED se necessário

// LCD
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Variáveis
bool mqttStatus = false;
bool relayState = false; // Estado inicial do relé (desligado)

// Objetos
WiFiClient wifiClient;
PubSubClient client(wifiClient);

// Protótipos
bool connectMQTT();
void callback(char* topic, byte* payload, unsigned int length);
void toggleRelay(bool state);
void dht_sensor_getdata();

void setup() {
  Serial.begin(9600);

  // Inicialização da conexão WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("Conectado à rede WiFi!");

  // Inicialização da conexão MQTT
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  mqttStatus = connectMQTT();

  // Configuração do pino do relé
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW); // Desliga o relé inicialmente

  // Inicializa o sensor DHT
  dht.begin();
  
  // Inicializa o display LCD
  lcd.init();
  lcd.backlight();
}

void loop() {
  // Atualiza dados do sensor DHT e exibe no LCD
  dht_sensor_getdata();
  
  // Mantém a conexão MQTT
  if (mqttStatus) {
    if (!client.connected()) {
      mqttStatus = connectMQTT();
    }
    client.loop();
  }
  
  // Adiciona um pequeno delay para evitar leituras muito frequentes
  delay(2000);
}

bool connectMQTT() {
  byte tentativa = 0;
  while (!client.connected() && tentativa < 5) {
    if (client.connect("arduinoClient", mqtt_username, mqtt_password)) {
      Serial.println("Conexão bem-sucedida ao broker MQTT!");
      client.subscribe(topic);
      return true;
    } else {
      Serial.print("Falha ao conectar: ");
      Serial.println(client.state());
      Serial.print("Tentativa: ");
      Serial.println(tentativa);
      delay(2000);
      tentativa++;
    }
  }
  Serial.println("Não foi possível conectar ao broker MQTT");
  return false;
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensagem recebida no tópico: ");
  Serial.println(topic);

  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("Mensagem: ");
  Serial.println(message);

  if (message.equals("ligar")) {
    toggleRelay(false);
  } else if (message.equals("desligar")) {
    toggleRelay(true);
  }
}

void toggleRelay(bool state) {
  relayState = state;
  digitalWrite(relayPin, state ? HIGH : LOW);
  client.publish(topic, state ? "ligado" : "desligado");
}

void dht_sensor_getdata() {
  float hm = dht.readHumidity();
  Serial.print("Umidade: ");
  Serial.println(hm);
  float temp = dht.readTemperature();
  Serial.print("Temperatura: ");
  Serial.println(temp);

  // Atualiza o LED com base na umidade e temperatura lidas
  if (temp > 30.0) {
    digitalWrite(LED, LOW); // Liga o LED se a temperatura for maior que 30 graus
  } else {
    digitalWrite(LED, HIGH); // Desliga o LED se a temperatura for menor ou igual a 30 graus
  }

  // Exibe os valores no LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(temp);
  lcd.print(" C");
  lcd.setCursor(0, 1);
  lcd.print("Umidade: ");
  lcd.print(hm);
  lcd.print(" %");

  // Converte os valores para String
  String tempString = String(temp, 2);
  String humString = String(hm, 2);

  // Publica os valores no broker MQTT
  client.publish("2bqsvw6678/temperatura2505", tempString.c_str());
  client.publish("2bqsvw6678/humidade2505", humString.c_str());
}
```

Em resumo, o projeto de Automação Residencial para Preparo de Café Inteligente oferece uma solução prática e eficiente para o preparo de café, combinando automação, conectividade e personalização para proporcionar uma experiência superior aos usuários.
