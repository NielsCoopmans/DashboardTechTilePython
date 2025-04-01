import json
import random
import time
from mqtt_config import client  # Importing the MQTT client from the shared config

# Generate unique device IDs
def generate_unique_device_ids(count):
    letters = ["G","F","E", "D", "C", "B", "A"]
    numbers = list(range(1, 21))  # Numbers from 1 to 20
    ids = [f"{letter}{num:02d}" for letter in letters for num in numbers]
    random.shuffle(ids)
    return ids[:count]  # Ensure uniqueness by limiting count

device_ids = generate_unique_device_ids(144)

def generate_ip():
    return f"192.168.1.{random.randint(1, 100)}"

def get_random_load():
    return f"{random.uniform(0, 100):.2f}%"

def get_random_ram():
    return f"{random.uniform(0, 8):.2f}GB"

def get_random_disk():
    return f"{random.uniform(0, 500):.2f}GB"

def get_random_temp():
    return f"{random.uniform(30, 70):.2f}"

# Create a list of 144 unique devices
rpi_devices = [
    {
        "id": device_id,
        "ip": generate_ip(),
        "status": "1"
    }
    for device_id in device_ids
]

def publish_rpi_data():
    while True:
        for device in rpi_devices:
            status_roll = random.random()
            if status_roll < 0.05:
                device["status"] = "0"
            elif status_roll < 0.1:
                device["status"] = "0.5"
            else:
                device["status"] = "1"

            data = {
                "id": device["id"],
                "ip": device["ip"],
                "status": device["status"],
                "cpuLoad": get_random_load(),
                "ram": get_random_ram(),
                "diskUsage": get_random_disk(),
                "temp": get_random_temp(),
            }

            client.publish("rpi/data", json.dumps(data))
            print("Published RPi Data:", data)

        time.sleep(1)  # Ensure all devices publish before next batch

def on_message(client, userdata, message):
    topic_parts = message.topic.split("/")
    if len(topic_parts) < 4:
        return
    _, __, device_id, command = topic_parts

    device = next((rpi for rpi in rpi_devices if rpi["id"] == device_id), None)
    if device:
        if command == "shutdown":
            device["status"] = "Disabled"
            print(f"{device['id']} is shutting down.")
        elif command == "reboot":
            device["status"] = "Running"
            print(f"{device['id']} is rebooting.")

        client.publish("rpi/data", json.dumps(device))

client.on_message = on_message

# Subscribe to control commands
def on_connect(client, userdata, flags, rc):
    for device in rpi_devices:
        client.subscribe(f"rpi/control/{device['id']}/#")

client.on_connect = on_connect

# Main entry point
if __name__ == "__main__":
    print("Mock Raspberry Pis connected to MQTT!")
    client.loop_start()
    publish_rpi_data()
