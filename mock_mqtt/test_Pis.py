import json
import time
import random
from mqtt_config import client  # Ensure this is the same config used in your main script

def on_message(client, userdata, message):
    """Callback function to handle received MQTT messages."""
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        print(f"Received from {message.topic}: {payload}")
    except json.JSONDecodeError:
        print(f"Invalid JSON from {message.topic}: {message.payload}")

def send_command(device_id, command):
    """Send a control command to a specific RPi."""
    topic = f"rpi/control/{device_id}/{command}"
    client.publish(topic, "")
    print(f"Sent '{command}' command to {device_id}")

def main():
    # Select a random test device ID
    test_device_id = "A05"

    # Attach message listener
    client.on_message = on_message

    # Subscribe to device data
    #client.subscribe("rpi/data/#")  # Listen to all RPi status updates
    #print(f"Listening for updates from all devices...")

    # Start MQTT loop
    #client.loop_start()

    try:
        time.sleep(2)  # Allow time for connection

        # Test shutdown command
        print(f"Testing shutdown on {test_device_id}...")
        send_command(test_device_id, "shutdown")

        time.sleep(5)  # Allow time for response

        # Test reboot command
        print(f"Testing reboot on {test_device_id}...")
        send_command(test_device_id, "reboot")

        time.sleep(5)  # Allow time for response

    except KeyboardInterrupt:
        print("\nTest interrupted by user.")

    finally:
        client.loop_stop()
        client.disconnect()
        print("MQTT test completed.")

if __name__ == "__main__":
    main()
