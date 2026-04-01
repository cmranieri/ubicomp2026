from machine import Pin, lightsleep, deepsleep
import time

led = Pin(4, Pin.OUT)

# Ligar LED por 3 segundos
led.on()
time.sleep(3)

while True:
    # piscando em modo ativo
    for i in range(6):
        led.on()
        time.sleep(0.3)
        led.off()
        time.sleep(0.3)

    # modo sleep
    # lightsleep(3000)
    # deepsleep(3000)
