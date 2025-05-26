import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np


def rolling_average(data, window_size=1):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')


def fetch_and_plot(device_id, hours=6, average_window=5):
    # Connect to SQLite DB
    conn = sqlite3.connect("rpi_data.db")
    cursor = conn.cursor()

    # Filter by timestamp (last N hours)
    cutoff = int((datetime.now() - timedelta(hours=hours)).timestamp())

    cursor.execute("""
        SELECT id, cpuLoad, cpuTemp, ram, diskUsage, timestamp
        FROM rpi_data
        WHERE id = ? AND timestamp >= ?
        ORDER BY timestamp ASC
    """, (device_id, cutoff))
    rows = cursor.fetchall()
    conn.close()

    # Process data
    timestamps = []
    cpu_loads = []
    cpu_temps = []
    rams = []
    disk_usages = []

    for row in rows:
        _, cpu_load_str, cpu_temp_str, ram_str, disk_usage_str, ts = row
        try:
            cpu_load = float(cpu_load_str.strip('%'))
            cpu_temp = float(cpu_temp_str)
            ram = float(ram_str.lower().replace('gb', '').strip())
            disk_usage = float(disk_usage_str.lower().replace('gb', '').strip())

            timestamps.append(datetime.fromtimestamp(ts))
            cpu_loads.append(cpu_load)
            cpu_temps.append(cpu_temp)
            rams.append(ram)
            disk_usages.append(disk_usage)
        except ValueError:
            continue

    # If too few points for averaging, skip smoothing
    if len(cpu_loads) < average_window:
        avg_cpu_loads = cpu_loads
        avg_cpu_temps = cpu_temps
        avg_rams = rams
        avg_disks = disk_usages
        avg_times = timestamps
    else:
        avg_cpu_loads = rolling_average(cpu_loads, average_window)
        avg_cpu_temps = rolling_average(cpu_temps, average_window)
        avg_rams = rolling_average(rams, average_window)
        avg_disks = rolling_average(disk_usages, average_window)
        avg_times = timestamps[average_window - 1:]  # match data size

    # Plotting
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(avg_times, avg_cpu_loads, label="CPU Load (%)", color='blue')
    plt.ylabel("CPU Load (%)")
    plt.title(f"RPi Metrics Over Last {hours} Hours — {device_id}")
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(avg_times, avg_cpu_temps, label="CPU Temp (°C)", color='red')
    plt.ylabel("CPU Temp (°C)")
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(avg_times, avg_rams, label="RAM (GB)", color='green')
    plt.plot(avg_times, avg_disks, label="Disk Usage (GB)", color='purple')
    plt.ylabel("GB")
    plt.xlabel("Time")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    device_id = "TECHDASH"
    fetch_and_plot(device_id, hours=6, average_window=1)
