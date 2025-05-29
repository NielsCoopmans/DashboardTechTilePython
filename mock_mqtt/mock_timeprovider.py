import json
import random
import time
from datetime import datetime
from mqtt_config import client  # Importing the MQTT client from the shared config

# Time provider data publishing
def publish_time_provider_data():
    interval = 1  # 1000 milliseconds
    while True:
        time_provider_id = "TimeProvider-1"

        data = {
            "id": time_provider_id,
            "status": "active",
            "lastSync": datetime.utcnow().isoformat(),
        }

        client.publish("timeprovider/data", json.dumps(data))
        print("Published Time Provider:", data)

        time.sleep(interval)

# Main entry point
if __name__ == "__main__":
    publish_time_provider_data()
