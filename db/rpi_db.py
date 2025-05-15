import json
import time
import sqlite3

from mqtt_config import client  # import the MQTT client from your mqtt_config.py

# === Database Setup ===
conn = sqlite3.connect("rpi_data.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS rpi_data (
        id TEXT,
        cpu_load TEXT,
        ram TEXT,
        disk_usage TEXT,
        cpu_temp TEXT,
        ip TEXT,
        timestamp INTEGER
    )
""")
conn.commit()

# === Data Insertion ===
def store_data(data):
    cursor.execute("INSERT INTO rpi_data VALUES (?, ?, ?, ?, ?, ?, ?)", (
        data.get("id", "unknown"),
        data.get("cpuLoad", "0%"),
        data.get("ram", "0GB"),
        data.get("diskUsage", "0GB"),
        data.get("cpuTemp", "0.0"),
        data.get("ip", "0.0.0.0"),
        int(time.time())
    ))
    conn.commit()

# === Override the on_message callback to add DB storage for rpi/data ===
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"Received message on {msg.topic}: {data}")

        if msg.topic == "rpi/data":
            store_data(data)

    except json.JSONDecodeError:
        print(f"Invalid JSON received on {msg.topic}: {msg.payload.decode()}")
    except Exception as e:
        print(f"Error processing message on {msg.topic}: {e}")

client.on_message = on_message

if __name__ == "__main__":
    client.loop_forever()
