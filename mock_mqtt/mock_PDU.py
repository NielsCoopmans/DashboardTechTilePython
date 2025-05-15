import json
import time
import random
from mqtt_config import client


def publish_pdu_data():
    interval = 0.7  # 700 milliseconds
    while True:
        pdu_id = f"PDU-{random.randint(1, 2)}"
        port = random.randint(1, 8)

        data = {
            "id": pdu_id,
            "port": port,
            "status": "Enabled" if random.random() > 0.2 else "Disabled",
            "current": f"{random.uniform(0, 10):.2f}A",
            "voltage": "230V",
            "power": f"{random.uniform(0, 200):.2f}W",
            "frequency": "50Hz",
        }

        client.publish("pdu/data", json.dumps(data))
        print("Published PDU:", data)

        time.sleep(interval)


if __name__ == "__main__":
    publish_pdu_data()
