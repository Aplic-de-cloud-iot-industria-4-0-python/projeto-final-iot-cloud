# Instruções para Utilização do Projeto Cafeteira IoT

Bem-vindo ao projeto **Cafeteira IoT**! Este guia fornecerá as instruções necessárias para configurar o ambiente, instalar as bibliotecas necessárias e utilizar o projeto de forma eficaz.

## 1. Configuração do Ambiente

### 1.1. Instalação do Arduino IDE

1. Baixe o Arduino IDE do site oficial: [Arduino IDE Download](https://www.arduino.cc/en/software).
2. Siga as instruções de instalação para o seu sistema operacional (Windows, macOS, Linux).

### 1.2. Adição da Placa ESP8266

1. Abra o Arduino IDE.
2. Vá para **File** > **Preferences**.
3. No campo **Additional Boards Manager URLs**, adicione o seguinte URL:

[http://arduino.esp8266.com/stable/package_esp8266com_index.json]()

e para o `ESP32`

[https://dl.espressif.com/dl/package_esp32_index.json]() 

4. Vá para **Tools** > **Board** > **Boards Manager**.
5. Pesquise por "ESP8266" e instale a placa ESP8266.

## 2. Instalação das Bibliotecas Necessárias

Para utilizar o projeto Cafeteira IoT, você precisará instalar as seguintes bibliotecas:

### 2.1. Biblioteca DHT

1. No Arduino IDE, vá para **Sketch** > **Include Library** > **Manage Libraries**.
2. Pesquise por "DHT sensor library" e instale a biblioteca de Adafruit.

### 2.2. Biblioteca PubSubClient

1. No Arduino IDE, vá para **Sketch** > **Include Library** > **Manage Libraries**.
2. Pesquise por "PubSubClient" e instale a biblioteca de Nick O'Leary.

### 2.3. Biblioteca HD44780

1. No Arduino IDE, vá para **Sketch** > **Include Library** > **Manage Libraries**.
2. Pesquise por "hd44780" e instale a biblioteca de Bill Perry.

## 3. Configuração do Broker MQTT

1. Escolha um serviço de broker MQTT. Recomendações:
- **Mosquitto**: [Eclipse Mosquitto](https://mosquitto.org/)
- **HiveMQ**: [HiveMQ](https://www.hivemq.com/)
- **Adafruit IO**: [Adafruit IO](https://io.adafruit.com/)

2. Siga as instruções específicas do serviço escolhido para configurar o broker MQTT.

## 4. Subindo o Código para o ESP8266

1. Conecte seu ESP8266 ao computador via cabo USB.
2. Abra o Arduino IDE.
3. Carregue o código do projeto (disponível no repositório).
4. Vá para **Tools** > **Board** e selecione "Generic ESP8266 Module" ou o modelo específico do seu ESP8266.
5. Selecione a porta correta em **Tools** > **Port**.
6. Clique em **Upload** para carregar o código no ESP8266.

## 5. Utilizando o Projeto

### 5.1. Monitoramento e Controle

- **Monitoramento de Temperatura e Umidade**: Os dados são exibidos no LCD e publicados via MQTT.
- **Monitoramento do Nível de Água**: O nível de água é exibido no LCD e LEDs indicam o estado.
- **Controle da Cafeteira**: A cafeteira pode ser ligada/desligada via comandos MQTT.

### 5.2. Comandos MQTT

- **Ligar Cafeteira**: Envie o comando "ligar" para o tópico MQTT configurado.
- **Desligar Cafeteira**: Envie o comando "desligar" para o tópico MQTT configurado.

## 6. Trabalhando com C++ no Arduino

### 6.1. Estrutura Básica de um Sketch Arduino

```cpp
void setup() {
// Código de inicialização
}

void loop() {
// Código principal que roda em loop
}
```

### 6.2. Funções e Variáveis 
- **Variáveis Globais** : Declare variáveis que serão usadas em todo o código. 
- **Funções** : Crie funções para modularizar o código e facilitar a manutenção.
### 6.3. Interação com Sensores e Atuadores 
- **Leitura de Sensores** : Utilize funções como `analogRead()` e `digitalRead()` para ler dados dos sensores. 
- **Controle de Atuadores** : Utilize `digitalWrite()` para controlar LEDs e relés.
### 6.4. Bibliotecas 
- **Incluir Bibliotecas** : Utilize `#include <Biblioteca.h>` para incluir bibliotecas necessárias. 
- **Instância de Objetos** : Crie instâncias de objetos para sensores e atuadores.
## 7. Recursos e Referências 
- **Documentação Oficial do Arduino** : [Arduino Documentation]() 
- **Tutorial de MQTT com PubSubClient** : [PubSubClient Documentation]() 
- **Biblioteca DHT** : [Adafruit DHT Sensor Library](https://github.com/adafruit/DHT-sensor-library) 
- **Biblioteca HD44780** : [hd44780 Library](https://github.com/duinoWitchery/hd44780)

Para mais detalhes sobre a implementação e funcionalidades do projeto, acesse a documentação completa no GitHub:

[Documentação Completa do Projeto](https://github.com/Aplic-de-cloud-iot-industria-4-0-python/projeto-final-iot-cloud/wiki) 

Esperamos que estas instruções sejam úteis para configurar e utilizar o projeto Cafeteira IoT. Se tiver alguma dúvida ou sugestão, sinta-se à vontade para contribuir no repositório ou abrir uma issue.
