import json
import time
import random
from mqtt_config import client


def publish_pdu_data():
    interval = 10  # 10 seconden
    while True:
        pdu_number = random.randint(1, 2)
        pdu_id = f"pdu-{str(pdu_number).zfill(3)}"  # => "pdu-001", "pdu-002"
        port = random.randint(1, 24)

        # Data per PDU-poort
        pdu_port_data = {
            "id": pdu_id,
            "port": port,
            "status": "Enabled" if random.random() > 0.2 else "Disabled",
            "current": f"{random.uniform(0, 10):.2f}A",
            "voltage": "230V",
            "power": f"{random.uniform(0, 200):.2f}W"
        }

        # Algemene PDU-apparaatdata
        pdu_device_data = {
            "id": pdu_id,
            "systemCurrent": f"{random.uniform(0, 40):.2f}A",
            "systemVoltage": "230V",
            "systemPower": f"{random.uniform(200, 1000):.2f}W",
            "frequency": "50Hz"
        }

        # Publiceer aparte topics
        client.publish("pdu/port", json.dumps(pdu_port_data))
        print("Published to pdu/port:", pdu_port_data)

        client.publish("pdu/data", json.dumps(pdu_device_data))
        print("Published to pdu/data:", pdu_device_data)

        time.sleep(interval)


if __name__ == "__main__":
    publish_pdu_data()
