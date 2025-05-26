import json
import time
import psutil
import socket
import threading
import os
from mqtt_config import client

# === System Info Functions ===
def get_cpu_load(): return round(psutil.cpu_percent(interval=1), 4)
def get_ram_usage(): return round(psutil.virtual_memory().used / (1024 ** 3), 2)
def get_disk_usage(): return round(psutil.disk_usage('/').used / (1024 ** 3), 2)
def get_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return float(f.read()) / 1000
    except: return 0.0
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except: return "0.0.0.0"
def get_device_id():
    try:
        return socket.gethostname().replace("rpi-", "")
    except:
        return "unknown"

device_id = get_device_id().upper()
pending_commands = {}  # {request_id: command}

# === Publishing System Info ===
def publish_rpi_data():
    while True:
        data = {
            "id": device_id,
            "cpuLoad": f"{get_cpu_load()}%",
            "ram": f"{get_ram_usage()}GB",
            "diskUsage": f"{get_disk_usage()}GB",
            "cpuTemp": f"{get_temp()}",
            "ip": get_ip_address()
        }
        client.publish("rpi/data", json.dumps(data))
        time.sleep(60)

# === MQTT Message Handler ===
def on_message(client, userdata, msg):
    global pending_commands

    try:
        data = json.loads(msg.payload.decode())
    except:
        print(f"Invalid JSON on {msg.topic}")
        return

    topic_parts = msg.topic.split('/')
    if msg.topic == f"rpi/control/{device_id}":
        command = data.get("command")
        request_id = data.get("request_id")
        if command and request_id:
            print(f"CONTROL REQUEST: {command} (id: {request_id})")
            pending_commands[request_id] = command
            # Send ACK
            ack = {
                "request_id": request_id,
                "status": "received",
                "device_id": device_id
            }
            client.publish(f"rpi/control/ack/{device_id}", json.dumps(ack))
    elif msg.topic == f"rpi/control/confirm/{device_id}":
        request_id = data.get("request_id")
        if request_id in pending_commands:
            command = pending_commands.pop(request_id)
            print(f"Executing confirmed command: {command}")
            if command == "shutdown":
                os.system("sudo shutdown now")
            elif command == "reboot":
                os.system("sudo reboot")

# === MQTT Setup ===
client.subscribe(f"rpi/control/{device_id}")
client.subscribe(f"rpi/control/confirm/{device_id}")
client.on_message = on_message
client.loop_start()

if __name__ == "__main__":
    print(f"RPi {device_id} monitoring and control started.")
    publish_rpi_data()
