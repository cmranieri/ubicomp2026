from machine import Pin
import bluetooth
import time

led = Pin(2, Pin.OUT)
led.on()
ble = bluetooth.BLE()
ble.active(True)

thr = 3500

def get_name(adv):
    i = 0
    while i < len(adv):
        ln = adv[i]
        if ln == 0:
            return None
        tp = adv[i + 1]
        if tp == 9:  # Complete Local Name
            return bytes(adv[i + 2:i + 1 + ln]).decode()
        i += ln + 1
    return None


def irq(ev, data):
    if ev == 5:  # scan result
        addr_type, addr, adv_type, rssi, adv = data
        _, _, _, _, adv = data
        name = get_name(adv)
        if not name:
            return
        print("adv name:", name)

        if name and name.startswith("LDR:"):
            val = int(name.split(":")[1])
            if val < thr:
                led.on()
            else:
                led.off()

ble.irq(irq)

while True:
    print("scanning...")
    ble.gap_scan(2000, 30000, 30000)
    time.sleep(4)