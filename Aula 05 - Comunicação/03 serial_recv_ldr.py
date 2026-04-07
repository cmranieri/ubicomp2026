from machine import Pin, UART
import time

led = Pin(2, Pin.OUT)
uart = UART(1, baudrate=9600, tx=17, rx=16)

threshold = 3500

while True:
    if uart.any():
        line = uart.readline()
        if line:
            print(line)
            value = int(line.decode().strip())
            print(value)
            if value < threshold:
                led.on()
            else:
                led.off()
    time.sleep(0.05)