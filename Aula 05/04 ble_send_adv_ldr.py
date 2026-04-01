from machine import Pin, ADC
import bluetooth
import time
import struct

ble = bluetooth.BLE()
ble.active(True)

ldr = ADC(Pin(33))
ldr.atten(ADC.ATTN_11DB)

def mk_adv(name):
    b = name.encode()
    p = bytearray()
    p += struct.pack("BB", 2, 1) + b"\x06"
    p += struct.pack("BB", len(b) + 1, 9) + b
    return p

while True:
    val = ldr.read()
    name = "LDR:" + str(val)
    print("sending:", name)
    ble.gap_advertise(100000, adv_data=mk_adv(name))
    time.sleep(1)