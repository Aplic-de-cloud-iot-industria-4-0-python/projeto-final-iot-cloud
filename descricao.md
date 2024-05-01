# Descrição do Projeto: Automação Residencial para Preparo de Café Inteligente

O projeto de Automação Residencial para Preparo de Café Inteligente é uma solução inovadora que combina tecnologias de Internet das Coisas (IoT) e sensores ambientais para oferecer conveniência e eficiência na preparação do café. Através da integração de componentes eletrônicos e conectividade com a nuvem, o sistema proporciona uma experiência automatizada e personalizada para os usuários, garantindo a qualidade do café e adaptando-se às condições ambientais.

## Componentes Principais:

    Arduino Uno: O cérebro do sistema, responsável pelo controle e integração de todos os componentes.
    Sensor de Temperatura e Umidade: Monitora o ambiente e fornece dados em tempo real sobre as condições de temperatura e umidade.
    Display LCD: Exibe informações relevantes, como temperatura, umidade e status do sistema.
    Relé: Controla o funcionamento da cafeteira, permitindo ligá-la e desligá-la remotamente.
    LEDs Indicadores: Fornecem feedback visual sobre o status do sistema, como temperatura limite atingida.
    Potenciômetro: Permite ajustar configurações do sistema, como a temperatura máxima para acionar a cafeteira.

## Funcionalidades Principais:

    Controle Remoto da Cafeteira: Os usuários podem ligar e desligar a cafeteira remotamente através de um aplicativo ou interface web.
    Monitoramento Ambiental: O sistema monitora constantemente a temperatura e umidade do ambiente, garantindo condições ideais para o preparo do café.
    Agendamento Automático: A cafeteira pode ser programada para ligar automaticamente em horários específicos, como pela manhã às 07:00, para garantir que o café esteja pronto quando os usuários acordarem.
    Feedback Visual e de Status: LEDs indicadores fornecem feedback visual sobre o estado do sistema, como alertas de temperatura máxima atingida.
    Exibição de Informações: O display LCD mostra as leituras atuais de temperatura e umidade, além do status da cafeteira.
    Personalização: Os usuários podem ajustar as configurações do sistema, como a temperatura máxima para acionar a cafeteira, através do potenciômetro.

## Integração com IoT na Nuvem:

    Todas as informações coletadas pelo sistema são enviadas para uma plataforma de IoT na nuvem para armazenamento, análise e monitoramento remoto.
    Os usuários podem acessar o status do sistema e receber notificações em tempo real sobre eventos importantes, como falhas no sistema ou cafeteira pronta.

## Benefícios:

    Conveniência: Os usuários podem preparar café automaticamente e programar o sistema de acordo com suas preferências.
    Eficiência Energética: A cafeteira só é acionada quando as condições ambientais são ideais, economizando energia.
    Controle Remoto: Os usuários têm controle total sobre o sistema, podendo monitorar e controlar remotamente a cafeteira.
    Personalização: O sistema pode ser personalizado para atender às preferências individuais dos usuários, garantindo uma experiência de café sob medida.

Em resumo, o projeto de Automação Residencial para Preparo de Café Inteligente oferece uma solução inovadora e prática para o preparo de café, combinando automação, conectividade e personalização para proporcionar uma experiência superior aos usuários.

---

o protocolo de comunicação pode variar dependendo das necessidades específicas do sistema e das tecnologias utilizadas. Aqui estão algumas opções comuns de protocolos de comunicação que podem ser adequadas para esse tipo de projeto:

    MQTT (Message Queuing Telemetry Transport):
        MQTT é um protocolo leve de mensagens baseado em TCP/IP, ideal para comunicação entre dispositivos IoT devido à sua baixa sobrecarga e eficiência em redes com largura de banda limitada.
        Pode ser usado para enviar dados de sensores, status do sistema e comandos de controle entre o dispositivo Arduino e a plataforma de IoT na nuvem.
        Oferece suporte a publicação/assinatura de tópicos, o que permite uma comunicação assíncrona entre os dispositivos e a nuvem.

    HTTP (Hypertext Transfer Protocol):
        HTTP é um protocolo de comunicação amplamente utilizado na web para transferência de dados entre clientes e servidores.
        Pode ser utilizado para comunicação entre o dispositivo Arduino e a nuvem através de requisições GET, POST e PUT, enviando e recebendo dados JSON, por exemplo.
        É mais comumente usado em ambientes onde a compatibilidade com a infraestrutura web existente é importante.

    CoAP (Constrained Application Protocol):
        CoAP é um protocolo de aplicação da Internet projetado para dispositivos com restrições de recursos, como dispositivos IoT.
        Ele permite a comunicação eficiente e assíncrona entre dispositivos em redes com restrições de largura de banda e energia.
        Pode ser uma opção adequada para ambientes onde a eficiência de recursos é uma prioridade.

    WebSockets:
        WebSockets é um protocolo de comunicação bidirecional, full-duplex, baseado em TCP, que permite a comunicação interativa em tempo real entre clientes e servidores.
        Pode ser utilizado para estabelecer uma conexão persistente entre o dispositivo Arduino e a nuvem, permitindo a transmissão contínua de dados e notificações em tempo real.

```cpp
#include <Arduino_ConnectionHandler.h>
#include <ArduinoIoTCloud.h>
#include <Arduino_LPS22HB.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); // Endereço do LCD e tamanho

const int LED_VERDE_PIN = 2;
const int LED_VERMELHO_PIN = 3;
const int RELE_PIN = 4;
const int SENSOR_TEMPERATURA_UMIDADE_PIN = A1;
const int POTENCIOMETRO_PIN = A0;
const int DISPLAY_PINS[] = {5, 6, 7, 8, 9, 10, 11}; // Pinos do display de 7 segmentos

const int TEMPERATURA_UMIDADE_INTERVALO = 5000; // Intervalo de leitura de temperatura e umidade (em milissegundos)
const int DISPLAY_INTERVALO = 1000; // Intervalo de atualização do display (em milissegundos)
const int LIGAR_CAFE_HORA = 7; // Hora de ligar a cafeteira
const int TEMPERATURA_MAXIMA = 35; // Temperatura máxima para ligar a cafeteira

float temperatura;
float umidade;
int potValue;

void setup() {
  ArduinoCloud.setThingId("XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"); // Defina o ID do seu dispositivo
  ArduinoCloud.addProperty(temperatura, "Float", READ);
  ArduinoCloud.addProperty(umidade, "Float", READ);
  ArduinoCloud.addProperty(potValue, "Potenciometro", READWRITE);
  ArduinoCloud.addProperty(estado_led, "Estado_LED", READ);
  
  pinMode(LED_VERDE_PIN, OUTPUT);
  pinMode(LED_VERMELHO_PIN, OUTPUT);
  pinMode(RELE_PIN, OUTPUT);
  
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("Temperatura:");
  lcd.setCursor(0,1);
  lcd.print("Umidade:");
}

void loop() {
  ArduinoCloud.update();
  
  // Leitura de temperatura e umidade
  if (millis() - lastTempHumidityReading >= TEMPERATURA_UMIDADE_INTERVALO) {
    readTemperatureAndHumidity();
    lastTempHumidityReading = millis();
  }
  
  // Atualização do display
  if (millis() - lastDisplayUpdate >= DISPLAY_INTERVALO) {
    updateDisplay();
    lastDisplayUpdate = millis();
  }
  
  // Verificação da hora para ligar a cafeteira
  if (hour() == LIGAR_CAFE_HORA && temperatura < TEMPERATURA_MAXIMA) {
    digitalWrite(RELE_PIN, HIGH); // Liga a cafeteira
    delay(30000); // Liga por 30 segundos
    digitalWrite(RELE_PIN, LOW); // Desliga a cafeteira
  }
  
  // Verificação da temperatura para acender o LED vermelho
  if (temperatura >= TEMPERATURA_MAXIMA) {
    digitalWrite(LED_VERMELHO_PIN, HIGH);
  } else {
    digitalWrite(LED_VERMELHO_PIN, LOW);
  }
}

void readTemperatureAndHumidity() {
  // Código para ler temperatura e umidade do sensor
  temperatura = // leia temperatura do sensor
  umidade = // leia umidade do sensor
}

void updateDisplay() {
  lcd.setCursor(13, 0);
  lcd.print(temperatura);
  lcd.setCursor(9, 1);
  lcd.print(umidade);
}
```
    
