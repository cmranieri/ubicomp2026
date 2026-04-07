from machine import Pin, ADC
import bluetooth
import time
import struct

ble = bluetooth.BLE()
ble.active(True)

ldr = ADC(Pin(33))
ldr.atten(ADC.ATTN_11DB)

srv_uuid = bluetooth.UUID("e7b8c9d0-4a2e-4f9b-8c1e-123456789abc")
chr_uuid = bluetooth.UUID("a3f1d2c4-9b8e-4c7a-91d2-abcdef123456")

service = (
    srv_uuid,
    (
        (chr_uuid, bluetooth.FLAG_READ),
    ),
)

((val_handle,),) = ble.gatts_register_services((service,))

def adv_payload(name):
    b = name.encode()
    p = bytearray()
    p += struct.pack("BB", 2, 0x01) + b"\x06"
    p += struct.pack("BB", len(b) + 1, 0x09) + b
    return p

ble.gap_advertise(100000, adv_data=adv_payload("ESP32-LDR"))

while True:
    val = ldr.read()
    ble.gatts_write(val_handle, str(val))
    print("sent:", val)
    time.sleep(0.3)