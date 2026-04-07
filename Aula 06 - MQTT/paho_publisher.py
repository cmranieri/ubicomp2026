import random, time
import paho.mqtt.publish as publish


MQTT_BROKER = "127.0.0.1"        # IP or hostname of the MQTT broker
MQTT_PORT = 1883                 # Standard MQTT port
MQTT_TOPIC = "example/topic"     # Topic to publish messages to

# Optional: Authentication (uncomment and set values if needed)
# MQTT_USERNAME = "<USERNAME>"
# MQTT_PASSWORD = "<PASSWORD>"



def virtual_sensor(mean=0, std=1):
    value = random.gauss(mean,std)
    return value
    

def publish_message(data, topic):
    """Publish a message to a specific MQTT topic."""
    try:
        publish.single(
            topic=topic,
            payload=data,
            hostname=MQTT_BROKER,
            port=MQTT_PORT,
            # Uncomment below if using authentication
            # auth={'username': MQTT_USERNAME, 'password': MQTT_PASSWORD}
        )
    except Exception as e:
        print(f"Error publishing message: {e}")



if __name__ == '__main__':
    while True:
        value = virtual_sensor()        
        print(f"Publishing to MQTT broker at {MQTT_BROKER}:{MQTT_PORT} on topic '{MQTT_TOPIC}'")
        publish_message(value, MQTT_TOPIC)
        time.sleep(0.5)
