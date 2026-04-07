import network
import time
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# LDR
adc = ADC(Pin(34))

# Wi-Fi
WIFI_SSID = "network_ssid"
WIFI_PASSWORD = "network_passwd"

# MQTT
MQTT_BROKER = "192.168.1.1"   # IP do computador ou Raspberry Pi com broker
MQTT_PORT = 1883
MQTT_CLIENT_ID = b"esp32_ldr"
MQTT_TOPIC = b"casa/ldr"


wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

while not wifi.isconnected():
    time.sleep(0.5)
print(wifi.ifconfig()[0])


client = MQTTClient(
    client_id=MQTT_CLIENT_ID,
    server=MQTT_BROKER,
    port=MQTT_PORT
)
client.connect()
print("MQTT ok")


while True:
    try:
        value = adc.read()
        print(value)
        msg = str(value)
        client.publish(MQTT_TOPIC, msg)
        print("Published:", msg)
        time.sleep(0.5)

    except Exception as e:
        print("Error:", e)
        time.sleep(2)
        connect_wifi()
        client = connect_mqtt()