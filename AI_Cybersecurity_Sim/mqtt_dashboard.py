<<<<<<< HEAD
import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
from collections import deque
import time

# MQTT settings
broker = "localhost"
topic = "iot/sensor/data"

# Data storage
temp_data = deque(maxlen=50)
hum_data = deque(maxlen=50)
air_data = deque(maxlen=50)
motion_data = deque(maxlen=50)
timestamps = deque(maxlen=50)

# Plot setup
plt.ion()
fig, axs = plt.subplots(2, 2, figsize=(10, 6))
plt.suptitle("🌐 Live IoT Sensor Dashboard")

def update_plots():
    axs[0, 0].cla()
    axs[0, 1].cla()
    axs[1, 0].cla()
    axs[1, 1].cla()

    axs[0, 0].plot(timestamps, temp_data, 'r-', label="Temperature (°C)")
    axs[0, 1].plot(timestamps, hum_data, 'b-', label="Humidity (%)")
    axs[1, 0].plot(timestamps, air_data, 'g-', label="Air Quality Index")
    axs[1, 1].bar(["Detected", "None"], [motion_data.count("detected"), motion_data.count("none")], color=['orange', 'gray'])

    axs[0, 0].legend()
    axs[0, 1].legend()
    axs[1, 0].legend()
    axs[1, 1].set_title("Motion Count")

    plt.tight_layout()
    plt.draw()
    plt.pause(0.1)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    timestamps.append(time.strftime("%H:%M:%S"))
    temp_data.append(payload["temperature"])
    hum_data.append(payload["humidity"])
    air_data.append(payload["air_quality"])
    motion_data.append(payload["motion"])

    update_plots()

client = mqtt.Client()
client.on_message = on_message
client.connect(broker, 1883, 60)
client.subscribe(topic)

print("✅ Dashboard running... Visualizing IoT data live")
client.loop_forever()
=======
import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt
from collections import deque
import time

# MQTT settings
broker = "localhost"
topic = "iot/sensor/data"

# Data storage
temp_data = deque(maxlen=50)
hum_data = deque(maxlen=50)
air_data = deque(maxlen=50)
motion_data = deque(maxlen=50)
timestamps = deque(maxlen=50)

# Plot setup
plt.ion()
fig, axs = plt.subplots(2, 2, figsize=(10, 6))
plt.suptitle("🌐 Live IoT Sensor Dashboard")

def update_plots():
    axs[0, 0].cla()
    axs[0, 1].cla()
    axs[1, 0].cla()
    axs[1, 1].cla()

    axs[0, 0].plot(timestamps, temp_data, 'r-', label="Temperature (°C)")
    axs[0, 1].plot(timestamps, hum_data, 'b-', label="Humidity (%)")
    axs[1, 0].plot(timestamps, air_data, 'g-', label="Air Quality Index")
    axs[1, 1].bar(["Detected", "None"], [motion_data.count("detected"), motion_data.count("none")], color=['orange', 'gray'])

    axs[0, 0].legend()
    axs[0, 1].legend()
    axs[1, 0].legend()
    axs[1, 1].set_title("Motion Count")

    plt.tight_layout()
    plt.draw()
    plt.pause(0.1)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    timestamps.append(time.strftime("%H:%M:%S"))
    temp_data.append(payload["temperature"])
    hum_data.append(payload["humidity"])
    air_data.append(payload["air_quality"])
    motion_data.append(payload["motion"])

    update_plots()

client = mqtt.Client()
client.on_message = on_message
client.connect(broker, 1883, 60)
client.subscribe(topic)

print("✅ Dashboard running... Visualizing IoT data live")
client.loop_forever()
>>>>>>> 73a22d491c063849a58ac9d3bd9d22a961f91bcb
