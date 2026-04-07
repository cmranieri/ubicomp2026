# Guia rápido para MQTT

## Broker Mosquitto

Um broker MQTT é o componente central do protocolo MQTT, responsável por receber mensagens de clientes (*publishers*) e distribuí-las aos clientes interessados (*subscribers*). Existem diferentes brokers disponíveis, correspondentes a implementações independentes do protocolo MQTT. O Eclipse Mosquitto é uma opção amplamente adotada por ser leve, de fácil configuração, compatível com o padrão MQTT, estável e open source, o que o torna adequado tanto para testes locais quanto para aplicações reais de pequeno e médio porte.

Para informações sobre a instalação do Mosquitto em diferentes sistemas operacionais, acesse:
https://mosquitto.org/download/


### Subindo o broker

Para subir o broker, considerando que o diretório em que se encontra o binário executável esteja no path do sistema, a sintaxe básica é simplesmente:

```bash
mosquitto
```

Por padrão, o comando acima irá executar um broker local que não aceita conexões remotas. O broker estará rodando em ```localhost```, na porta ```1883```.

Para configurar o broker, você pode usar um arquivo de configuração, especificando-o com uso do argumento ```-c```.

```bash
mosquitto -c filename.conf
```

Onde ```filename.conf``` é o nome do arquivo de configuração.


### Arquivo de configuração

Algumas configurações comuns a se fazer seriam (i) executar um broker que permita acesso remoto e (ii) implementar um procedimento de autenticação. Para permitir acesso remoto, o arquivo de configuração deve configurar o listener sem limitá-lo ao localhost, como no seguinte exemplo:

```
allow_anonymous true
listener 1883
```

O exemplo acima permite que qualquer cliente na rede possa se conectar ao broker, sem necessidade de autenticação. Para configurar a autenticação com uso de senha, usar:

```
allow_anonymous false
password_file <caminho_para_arquivo_de_senha>
```

O arquivo com senha deve ser gerado com uso do programa ```mqtt_passwd```, incluído na instalação do Mosquitto.

```
mosquitto_passwd -c <nome_do_arquivo>
```

O comando acima permitirá criar um usuário com senha, e deve ser o arquivo especificado como ```password_file``` no arquivo de configuração do broker.



### Publicando e subscrevendo-se via terminal

É possível publicar em um tópico ou subscrever-se usando programas de terminal incluídos na instalação do Mosquitto. Como exemplo básico, vamos publicar uma mensagem simples no tópico ```hello``` usando um broker local. Em um terminal, suba o broker:

```bash
mosquitto
```

Deixe rodando e, em um segundo terminar, subscreva-se ao tópico:

```bash
mosquitto_sub -t "hello"
```

Em um terceiro terminal, publique no tópico:

```bash
mosquitto_pub -t "hello" -m "hello world"
```

O conteúdo publicado será exibido pelo terminal que está rodando ```mosquitto_sub```. Caso seja necessário autenticar-se, usar os seguintes argumentos (semelhante para o ```mosquitto_pub```):

```bash
mosquitto_sub -h <host> -p 1883 -t <topico> -u <usuario> -P <senha>
```

No exemplo, também estamos especificando o host (que pode ser remoto) e a porta (que pode ser outra que não a 1883). Exemplo concreto:

```bash
mosquitto_sub -h 192.168.0.10 -t sensores/temp -u caetano -P 1234
```


## Usando MQTT em Python

Para usar MQTT em Python, é necessário instalar um pacote para isso, como o ```mqtt_paho```.

```bash
pip install paho-mqtt
```


## Usando MQTT no ESP32 com MicroPython

Será necessário usar o pacote ```mpremote``` para instalar pacotes Python no ESP32. No caso, utilizaremos o pacote ```umqtt```. Com o ESP32 conectado ao computador, rode:

```bash
pip install mpremote
mpremote connect auto repl
mpremote mip install umqtt.simple
```



