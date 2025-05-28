import json
import time
import random
import yaml
from mqtt_config import client


def load_midspan_config(path='hosts.yaml'):
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    return config["all"]["vars"]['midspans']


def generate_poepoort_data(midspan_id, port):
    return {
        "id": midspan_id,
        "port": port,
        "status": "Enabled" if random.random() > 0.3 else "Disabled",
        "power": f"{random.uniform(0, 30):.2f}W",
        "maxPower": f"{random.uniform(30, 60):.2f}W",
        "class": random.randint(0, 8)
    }


def generate_midspan_data(midspan_id):
    return {
        "id": midspan_id,
        "totalPowerConsumption": f"{random.uniform(0, 100):.2f}W",
        "maxAvailablePowerBudget": "500W",
        "systemVoltage": "48V",
        "temperature": f"{random.uniform(20, 40):.2f}°C",
        "status": "Operational" if random.random() > 0.1 else "Fault"
    }


def publish_midspan_data():
    midspans = load_midspan_config()
    interval = 10  # seconden tussen updates

    while True:
        for midspan_id, data in midspans.items():
            nr_ports = data.get("nr-ports", 24)

            # Publiceer per poort
            for port in range(1, nr_ports + 1):
                poepoort_data = generate_poepoort_data(midspan_id, port)
                client.publish("midspan/poepoort", json.dumps(poepoort_data))
                print("Published to midspan/poepoort:", poepoort_data)

            # Publiceer algemene midspan-data
            midspan_data = generate_midspan_data(midspan_id)
            client.publish("midspan/data", json.dumps(midspan_data))
            print("Published to midspan/data:", midspan_data)

        time.sleep(interval)


if __name__ == "__main__":
    publish_midspan_data()
