import json
import time
import uuid
from mqtt_config import client

def on_message(client, userdata, message):
    """Handle incoming ACK messages."""
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        topic_parts = message.topic.split("/")
        if topic_parts[0] == "rpi" and topic_parts[1] == "control" and topic_parts[2] == "ack":
            print(f"[ACK] Received from {message.topic}: {payload}")

            # Send confirmation
            confirm_topic = f"rpi/control/confirm/{payload['device_id']}"
            confirm_payload = {
                "request_id": payload["request_id"]
            }
            client.publish(confirm_topic, json.dumps(confirm_payload))
            print(f"[CONFIRM] Sent confirmation for {payload['request_id']} to {confirm_topic}")
    except json.JSONDecodeError:
        print(f"Invalid JSON from {message.topic}: {message.payload}")

def send_command(device_id, command):
    """Send a command request with a unique request_id."""
    topic = f"rpi/control/{device_id}"
    request_id = str(uuid.uuid4())
    payload = {
        "request_id": request_id,
        "command": command
    }
    client.publish(topic, json.dumps(payload))
    print(f"[SEND] Sent '{command}' to {device_id} with request ID {request_id}")

def main():
    test_device_id = ("T08")

    client.on_message = on_message
    client.subscribe(f"rpi/control/ack/{test_device_id}")
    client.loop_start()

    try:
        time.sleep(2)


        print(f"Testing reboot on {test_device_id}...")
        send_command(test_device_id, "reboot")
        time.sleep(10)

    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("MQTT test completed.")

if __name__ == "__main__":
    main()
