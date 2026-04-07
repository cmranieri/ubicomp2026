from machine import Pin, ADC, UART
import time

ldr = ADC(Pin(33))
ldr.atten(ADC.ATTN_11DB)

uart = UART(1, baudrate=9600, tx=17, rx=16)

while True:
    value = ldr.read()
    print(value)
    uart.write(str(value) + "\n")
    time.sleep(0.5)