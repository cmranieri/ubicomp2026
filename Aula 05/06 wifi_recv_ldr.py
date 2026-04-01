from machine import Pin
import network
import socket
import time

led = Pin(2, Pin.OUT)
led.on()
threshold = 3500

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("caetano", "ubi6206comp")

while not wifi.isconnected():
    time.sleep(0.5)
print(wifi.ifconfig()[0])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 12345))

s.settimeout(2)


print("bind ok")


while True:
    try:
        print("esperando...")
        dados, addr = s.recvfrom(32)
        print("recebi", dados, addr)
        data, addr = s.recvfrom(32)
        value = int(data.decode())
        if value < threshold:
            led.on()
        else:
            led.off()
    except Exception as e:
        print("timeout ou erro:", e)
        


