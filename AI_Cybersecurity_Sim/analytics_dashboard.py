# analytics_dashboard.py
import json
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime

# MQTT broker details
BROKER = "localhost"
TOPICS = [("iot/temperature", 0), ("iot/network", 0)]

# Data storage
temperature_data = []
network_data = []
timestamps = []
alerts = []

# Alert log file
LOG_FILE = "alerts.log"

# Thresholds (can be tuned)
TEMP_MAX = 30.0
NETWORK_MAX = 250

# Max points to keep in the live plot
MAX_POINTS = 50

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print("📡 Connected to MQTT Broker")
    client.subscribe(TOPICS)

def on_message(client, userdata, msg):
    global temperature_data, network_data, timestamps

    try:
        data = json.loads(msg.payload.decode())
        sensor = data.get("sensor")
        value = data.get("value")

        # Append timestamp and sensor value
        now_str = datetime.now().strftime("%H:%M:%S")
        timestamps.append(now_str)

        if sensor == "temperature":
            temperature_data.append(value)
            if value > TEMP_MAX:
                log_alert(f"⚠️ High Temperature Detected: {value:.2f}°C")

        elif sensor == "network":
            network_data.append(value)
            if value > NETWORK_MAX:
                log_alert(f"🚨 Possible Network Attack Detected: {value}")

        # Keep lists synchronized by trimming to the shortest available data length
        # (this prevents x/y length mismatch during plotting)
        max_len = min(len(timestamps), len(temperature_data), len(network_data))
        if max_len > 0:
            timestamps[:] = timestamps[-max_len:]
            temperature_data[:] = temperature_data[-max_len:]
            network_data[:] = network_data[-max_len:]

        # Also ensure we don't exceed MAX_POINTS (safety for performance)
        if len(timestamps) > MAX_POINTS:
            timestamps.pop(0)
            temperature_data.pop(0)
            network_data.pop(0)

    except Exception as e:
        print("Error in on_message:", e)

def log_alert(alert):
    timestamp = datetime.now().strftime("%H:%M:%S")
    alert_text = f"[{timestamp}] {alert}"
    # Safe UTF-8 logging (ignore characters that cannot be written)
    with open(LOG_FILE, "a", encoding="utf-8", errors="ignore") as f:
        f.write(alert_text + "\n")
    print(alert_text)

# Plot setup
plt.style.use("seaborn")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
fig.suptitle("AI Cybersecurity IoT Analytics Dashboard")

ax1.set_title("Temperature Sensor")
ax1.set_ylabel("°C")

ax2.set_title("Network Traffic Sensor")
ax2.set_ylabel("Packets/s")

def update_graph(frame):
    ax1.clear()
    ax2.clear()

    # Plot only when we have data
    if len(timestamps) > 0 and len(temperature_data) == len(timestamps):
        ax1.plot(timestamps, temperature_data, color="orange", label="Temperature")
    # draw threshold line always for clarity
    ax1.axhline(y=TEMP_MAX, color="red", linestyle="--", label="Temp Threshold")
    ax1.legend(loc="upper left")
    ax1.set_ylabel("°C")

    if len(timestamps) > 0 and len(network_data) == len(timestamps):
        ax2.plot(timestamps, network_data, color="red", label="Network Traffic")
    ax2.axhline(y=NETWORK_MAX, color="red", linestyle="--", label="Network Threshold")
    ax2.legend(loc="upper left")
    ax2.set_ylabel("Packets/s")

    # rotate x labels a bit for readability
    plt.setp(ax2.get_xticklabels(), rotation=30, ha="right")
    plt.tight_layout()

# Start MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_start()

# Animate the plot
ani = FuncAnimation(fig, update_graph, interval=1000)
plt.show()
