import paho.mqtt.client as mqtt
import random
import string
from paho.mqtt.client import CallbackAPIVersion

# Callback when client connects to the broker
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected to broker successfully.")
    else:
        print(f"Connection failed. Reason code: {reason_code}")

# Callback when a message is received from the broker
def on_message(client, userdata, msg, properties=None):
    print(f"Topic: {msg.topic} | Message: {msg.payload.decode()}")

# Generate a random MQTT client ID
def generate_client_id(length=8):
    characters = string.ascii_letters + string.digits
    return "client_" + ''.join(random.choice(characters) for _ in range(length))

# Configuration (edit these values as needed)
BROKER_ADDRESS = "127.0.0.1"     # Replace with broker IP or hostname
BROKER_PORT = 1883               # Standard MQTT port (can be changed)
TOPIC = "casa/ldr"          # Replace with topic you want to subscribe to

# Optional authentication (uncomment and configure if needed)
# USERNAME = "<USERNAME>"
# PASSWORD = "<PASSWORD>"

client_id = generate_client_id()
client = mqtt.Client(
    client_id=client_id,
    callback_api_version=CallbackAPIVersion.VERSION2
)

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Optional: Set authentication
# client.username_pw_set(USERNAME, PASSWORD)

# Optional: Enable TLS for secure connections
# client.tls_set()

try:
    print(f"Connecting to MQTT broker at {BROKER_ADDRESS}:{BROKER_PORT} with client ID: {client_id}")
    client.connect(BROKER_ADDRESS, BROKER_PORT)

    client.loop_start()
    client.subscribe(TOPIC)
    print(f"Subscribed to topic: {TOPIC}")

    # Keep the script running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nInterrupt received. Disconnecting...")
        client.loop_stop()
        client.disconnect()

except Exception as e:
    print(f"Connection error: {e}")
