import json
import time
import random
import paho.mqtt.client as mqtt

# MQTT Configuration
BROKER_HOST = "10.128.48.5"
BROKER_PORT = 1883
CLIENT_ID = f"client_{hex(random.getrandbits(64))[2:]}"
TOPICS = [
    "midspan/data",
    "pdu/data",
    "rpi/data",
    "timeprovider/data"
]

def on_connect(client, userdata, flags, reasonCode, properties=None):
    if reasonCode == 0:
        print("Connected to MQTT Broker!")
        for topic in TOPICS:
            client.subscribe(topic)
            print(f"Subscribed to {topic}")
    else:
        print(f"Failed to connect, reason code: {reasonCode}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"Received message on {msg.topic}: {data}")
    except json.JSONDecodeError:
        print(f"Invalid JSON received on {msg.topic}: {msg.payload.decode()}")

# Use modern callback API (version 5 is now default)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=CLIENT_ID, protocol=mqtt.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

if __name__ == "__main__":
    client.loop_forever()
