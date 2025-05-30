# MQTT Topics Documentation

This document provides a reference for all MQTT topics used in the system, including payload structures and expected values.

---

## 🖥️ `server/data`

### Description:

Publishes the current status of a server, including CPU, RAM, disk usage, and IP information.

### Payload Example:

```json
{
  "status": "active",
  "ip": "192.168.1.54",
  "cpuLoad": "67",
  "ram": "45",
  "internalDisk": "83",
  "raidDisk": "71",
  "cpuTemp": "45"
}
```

### Fields:

* `status`: `"active"` or `"inactive"`
* `ip`: IPv4 address
* `cpuLoad`: CPU usage percentage
* `ram`: RAM usage percentage
* `internalDisk`: Internal disk usage percentage
* `raidDisk`: RAID disk usage percentage
* `cpuTemp`: CPU temperature in Celsius

---

## 🔌 `midspan/poepoort`

### Description:

Publishes the power status for each individual PoE port on a midspan device.

### Payload Example:

```json
{
  "id": "midspan-001",
  "port": 3,
  "status": "active",
  "power": "12.30W",
  "maxPower": "60.00W",
  "class": 4
}
```

### Fields:

* `id`: Unique midspan ID (e.g., `midspan-001`)
* `port`: Port number (1–24 or 1–12)
* `status`: `"active"` or `"inactive"`
* `power`: Current power draw in watts
* `maxPower`: Maximum supported power draw
* `class`: PoE class (0–8)

---

## 🔧 `midspan/data`

### Description:

Publishes overall metrics of each midspan device.

### Payload Example:

```json
{
  "id": "midspan-001",
  "totalPowerConsumption": "83.20W",
  "maxAvailablePowerBudget": "500W",
  "systemVoltage": "48V",
  "temperature": "35.60°C",
  "status": "active"
}
```

### Fields:

* `id`: Unique midspan ID
* `totalPowerConsumption`: Sum of all port power draw
* `maxAvailablePowerBudget`: Device's power budget
* `systemVoltage`: System voltage
* `temperature`: Device temperature
* `status`: `"active"` or `"inactive"`

---

## 🔌 `pdu/port`

### Description:

Publishes the power metrics per PDU port.

### Payload Example:

```json
{
  "id": "pdu-001",
  "port": 8,
  "status": "active",
  "current": "3.15A",
  "voltage": "230V",
  "power": "140.25W"
}
```

### Fields:

* `id`: PDU ID (e.g., `pdu-001`)
* `port`: Port number
* `status`: active/inactive
* `current`: Current draw in amps
* `voltage`: Line voltage
* `power`: Current power draw

---

## ⚙️ `pdu/data`

### Description:

Publishes total metrics per PDU device.

### Payload Example:

```json
{
  "id": "pdu-001",
  "systemCurrent": "23.42A",
  "systemVoltage": "230V",
  "systemPower": "560.30W",
  "frequency": "50Hz",
  "status": "active"
}
```

### Fields:

* `id`: PDU device ID
* `systemCurrent`: Total current
* `systemVoltage`: System voltage
* `systemPower`: Total power usage
* `frequency`: AC frequency (e.g., 50Hz)
* `status`: active/inactive

---

## 📟 `rpi/data`

### Description:

Publishes live metrics from each Raspberry Pi.

### Payload Example:

```json
{
  "id": "A05",
  "cpuLoad": "10.20%",
  "ram": "0.92GB",
  "diskUsage": "6.42GB",
  "cpuTemp": "48.0",
  "ip": "192.168.1.77"
}
```

### Fields:

* `id`: Raspberry Pi ID
* `cpuLoad`: CPU usage
* `ram`: RAM used
* `diskUsage`: Disk used
* `cpuTemp`: CPU temperature (Celsius)
* `ip`: IP address

---
