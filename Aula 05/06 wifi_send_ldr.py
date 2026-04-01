from machine import Pin, ADC
import network
import socket
import time

ldr = ADC(Pin(33))
ldr.atten(ADC.ATTN_11DB)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("caetano", "ubi6206comp")

while not wifi.isconnected():
    time.sleep(0.5)

ip_dest = "192.168.1.3"   # coloque aqui o IP do outro ESP32
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    value = ldr.read()
    print(value)
    s.sendto(str(value).encode(), (ip_dest, port))
    time.sleep(1)
    