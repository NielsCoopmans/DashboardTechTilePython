import json
import time
import random
import paho.mqtt.client as mqtt

# MQTT Configuration
BROKER_URL = "mqtt://test.mosquitto.org"
CLIENT_ID = f"client_{hex(random.getrandbits(64))[2:]}"
TOPICS = [
    "midspan/data",
    "pdu/data",
    "rpi/data",
    "timeprovider/data"
]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        for topic in TOPICS:
            client.subscribe(topic)
            print(f"Subscribed to {topic}")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"Received message on {msg.topic}: {data}")
    except json.JSONDecodeError:
        print(f"Invalid JSON received on {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org", 1883, 60)

if __name__ == "__main__":
    client.loop_forever()
