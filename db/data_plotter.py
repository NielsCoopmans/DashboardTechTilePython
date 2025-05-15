import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime


def fetch_and_plot(device_id):
    # Connect to SQLite DB
    conn = sqlite3.connect("rpi_data.db")
    cursor = conn.cursor()

    # Fetch recent data for the given device_id
    cursor.execute("""
        SELECT id, cpu_load, cpu_temp, ram, disk_usage, timestamp
        FROM rpi_data
        WHERE id = ?
        ORDER BY timestamp DESC
        LIMIT 1000
    """, (device_id,))
    rows = cursor.fetchall()
    conn.close()

    # Process data
    timestamps = []
    cpu_loads = []
    cpu_temps = []
    rams = []
    disk_usages = []

    for row in reversed(rows):  # reverse to get chronological order
        _, cpu_load_str, cpu_temp_str, ram_str, disk_usage_str, ts = row
        try:
            cpu_load = float(cpu_load_str.strip('%'))
            cpu_temp = float(cpu_temp_str)

            # Process RAM (e.g., "1.5GB" -> 1.5)
            ram = float(ram_str.lower().replace('gb', '').strip())

            # Process disk usage (e.g., "15.7GB" -> 15.7)
            disk_usage = float(disk_usage_str.lower().replace('gb', '').strip())

            timestamps.append(datetime.fromtimestamp(ts))
            cpu_loads.append(cpu_load)
            cpu_temps.append(cpu_temp)
            rams.append(ram)
            disk_usages.append(disk_usage)

        except ValueError:
            continue

    # Plotting
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(timestamps, cpu_loads, label="CPU Load (%)", color='blue')
    plt.ylabel("CPU Load (%)")
    plt.title(f"RPi Metrics Over Time — {device_id}")
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(timestamps, cpu_temps, label="CPU Temp (°C)", color='red')
    plt.ylabel("CPU Temp (°C)")
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(timestamps, rams, label="RAM (GB)", color='green')
    plt.plot(timestamps, disk_usages, label="Disk Usage (GB)", color='purple')
    plt.ylabel("GB")
    plt.xlabel("Time")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    device_id = "TECHDASH"
    fetch_and_plot(device_id)
