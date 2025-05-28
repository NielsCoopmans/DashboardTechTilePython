import json
import time
import random
from mqtt_config import client

def generate_ip():
    return f"192.168.1.{random.randint(1, 100)}"

def get_random_percent():
    return f"{random.randint(0, 100)}%"

def get_random_gb(max_val):
    return f"{random.randint(0, max_val)}GB"

def get_random_temp():
    return f"{random.randint(30, 70)}"

def publish_server_data():
    interval = 10  # seconds
    while True:
        server_id = f"SERVER-{random.randint(1, 2)}"

        data = {
            "status": "Unknown",
            "ip": "0.0.0.0",
            "cpuLoad": "0%",
            "ram": "0%",
            "internalDisk": "0%",
            "raidDisk": "0%",
            "cpuTemp": "30"
        }

        # Simulate realistic values:
        if random.random() > 0.3:  # 70% chance the server is 'Working'
            data["status"] = "Working"
            data["ip"] = generate_ip()
            data["cpuLoad"] = get_random_percent()
            data["ram"] = get_random_percent()
            data["internalDisk"] = get_random_percent()
            data["raidDisk"] = get_random_percent()
            data["cpuTemp"] = get_random_temp()

        client.publish("server/data", json.dumps(data))
        print("Published to server/data:", data)

        time.sleep(interval)


if __name__ == "__main__":
    publish_server_data()
