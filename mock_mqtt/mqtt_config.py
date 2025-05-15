import json

import paho.mqtt.client as mqtt
import random

# MQTT Configuration
BROKER_URL = "10.128.48.5"
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

# Create MQTT client
client = mqtt.Client(client_id=CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_URL, 1883, 60)

# Export client for use in other scripts
__all__ = ["client"]
