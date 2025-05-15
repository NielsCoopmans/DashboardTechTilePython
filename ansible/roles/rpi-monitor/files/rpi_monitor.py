import json
import time
import psutil
import subprocess
import socket
from mqtt_config import client

def get_cpu_load():
    return round(psutil.cpu_percent(interval=1), 4)

def get_ram_usage():
    mem = psutil.virtual_memory()
    return round(mem.used / (1024 ** 3), 2)  # in GB

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return round(disk.used / (1024 ** 3), 2)  # in GB

def get_temp():
    try:
        output = subprocess.check_output(["/usr/bin/vcgencmd", "measure_temp"]).decode()
        return float(output.strip().replace("temp=", "").replace("'C", ""))
    except:
        return 0.0

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "0.0.0.0"

def get_device_id():
    try:
        hostname = socket.gethostname()
        device_id = hostname.replace("rpi-", "")
        return device_id
    except:
        return "unknown"

def publish_rpi_data():
    device_id = get_device_id()
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
        print("Published RPi Data:", data)
        time.sleep(10)

if __name__ == "__main__":
    print(f"Raspberry Pi {get_device_id()} connected to MQTT!")
    client.loop_start()
    publish_rpi_data()
