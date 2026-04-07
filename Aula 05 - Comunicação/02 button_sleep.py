from machine import Pin, deepsleep, lightsleep
import esp32
import time

led = Pin(4, Pin.OUT)
botao = Pin(33, Pin.IN, Pin.PULL_UP)

# configura wake-up pelo botão
esp32.wake_on_ext0(pin=botao, level=esp32.WAKEUP_ALL_LOW)

# modo normal por alguns segundos
for i in range(10):
    led.on()
    time.sleep(0.2)
    led.off()
    time.sleep(0.2)

# dorme e só acorda ao apertar o botão
#lightsleep()
deepsleep()