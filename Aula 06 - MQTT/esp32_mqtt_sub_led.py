import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# LED
led = Pin(2, Pin.OUT)

# Wi-Fi
WIFI_SSID = "network_ssid"
WIFI_PASSWORD = "network_passwd"

# MQTT
MQTT_BROKER = "192.168.1.1"   # IP do computador ou Raspberry Pi com broker
MQTT_PORT = 1883
MQTT_CLIENT_ID = b"esp32_led"
MQTT_TOPIC = b"casa/led"


wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

while not wifi.isconnected():
    time.sleep(0.5)
print(wifi.ifconfig()[0])


def on_message(topic, msg):
    print("Receuved:", topic, msg)
    led.toggle()


client = MQTTClient(
    client_id=MQTT_CLIENT_ID,
    server=MQTT_BROKER,
    port=MQTT_PORT
)
client.set_callback(on_message)
client.connect()
client.subscribe(MQTT_TOPIC)


while True:
    try:
        client.check_msg()   # checks for new messages
        time.sleep(0.1)
    except Exception as e:
        print("Error:", e)
        time.sleep(2)
        client.connect()
        client.subscribe(TOPIC)