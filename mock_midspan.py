import json
import time
import random
from mqtt_config import client  # Import the shared MQTT client


def publish_midspan_data():
    interval = 0.8  # 800 milliseconds (0.8 seconds)
    while True:
        midspan_id = f"Midspan-{random.randint(1, 3)}"
        port = random.randint(1, 8)

        data = {
            "id": midspan_id,
            "port": port,
            "status": "Enabled" if random.random() > 0.3 else "Disabled",
            "power": f"{random.uniform(0, 30):.2f}W",
            "maxPower": f"{random.uniform(30, 60):.2f}W",
            "class": random.randint(0, 8),
            "totalPowerConsumption": f"{random.uniform(0, 100):.2f}W",
            "maxAvailablePowerBudget": "500W",
            "systemVoltage": "48V",
            "temperature": f"{random.uniform(20, 40):.2f}°C",
        }

        client.publish("midspan/data", json.dumps(data))
        print("Published Midspan:", data)

        time.sleep(interval)


# Main entry point
if __name__ == "__main__":

    # Start publishing midspan data
    publish_midspan_data()
