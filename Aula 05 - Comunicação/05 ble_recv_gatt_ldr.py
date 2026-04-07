from machine import Pin
import bluetooth
import time

led = Pin(2, Pin.OUT)
led.on()
ble = bluetooth.BLE()
ble.active(True)

thr = 3500

srv_uuid = bluetooth.UUID("e7b8c9d0-4a2e-4f9b-8c1e-123456789abc")
chr_uuid = bluetooth.UUID("a3f1d2c4-9b8e-4c7a-91d2-abcdef123456")

conn = None
start = None
end = None
val_handle = None
peer_type = None
peer_addr = None

def get_name(adv):
    i = 0
    while i < len(adv):
        ln = adv[i]
        if ln == 0:
            return None
        tp = adv[i + 1]
        if tp == 0x09:
            return bytes(adv[i + 2:i + 1 + ln]).decode()
        i += ln + 1
    return None

def irq(ev, data):
    global conn, start, end, val_handle, peer_type, peer_addr

    if ev == 5:  # scan result
        addr_type, addr, adv_type, rssi, adv = data
        name = get_name(adv)
        if name == "ESP32-LDR":
            peer_type = addr_type
            peer_addr = bytes(addr)
            print("found")
            ble.gap_scan(None)

    elif ev == 7:  # connected
        conn, _, _ = data
        print("connected")
        ble.gattc_discover_services(conn)

    elif ev == 9:  # service result
        c, s, e, uuid = data
        if c == conn and bluetooth.UUID(uuid) == srv_uuid:
            start = s
            end = e
            print("service found")
            ble.gattc_discover_characteristics(conn, start, end)

    elif ev == 11:  # characteristic result
        c, _, vh, _, uuid = data
        if c == conn and bluetooth.UUID(uuid) == chr_uuid:
            val_handle = vh
            print("char found")

    elif ev == 15:  # read result
        c, vh, char_data = data
        if c == conn and vh == val_handle:
            val = int(bytes(char_data).decode())
            print("recv:", val)

            if val < thr:
                led.on()
            else:
                led.off()

ble.irq(irq)

print("scanning...")
ble.gap_scan(5000, 30000, 30000)

while peer_addr is None:
    time.sleep(0.1)

print("connecting...")
ble.gap_connect(peer_type, peer_addr)

while conn is None:
    time.sleep(0.1)

while val_handle is None:
    time.sleep(0.1)

while True:
    ble.gattc_read(conn, val_handle)
    time.sleep(0.3)