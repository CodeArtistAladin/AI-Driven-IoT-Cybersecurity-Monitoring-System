<<<<<<< HEAD
import paho.mqtt.client as mqtt
import time
import random
import json

broker = "localhost"
port = 1883

client = mqtt.Client()
client.connect(broker, port, 60)

print("✅ MQTT Publisher started... Sending simulated sensor data")

while True:
    data = {
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(40, 70), 2),
        "motion": random.choice(["detected", "none"]),
        "air_quality": round(random.uniform(50, 150), 2)
    }

    client.publish("iot/sensor/data", json.dumps(data))
    print("📡 Sent:", data)
    time.sleep(2)
=======
import paho.mqtt.client as mqtt
import time
import random
import json

broker = "localhost"
port = 1883

client = mqtt.Client()
client.connect(broker, port, 60)

print("✅ MQTT Publisher started... Sending simulated sensor data")

while True:
    data = {
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(40, 70), 2),
        "motion": random.choice(["detected", "none"]),
        "air_quality": round(random.uniform(50, 150), 2)
    }

    client.publish("iot/sensor/data", json.dumps(data))
    print("📡 Sent:", data)
    time.sleep(2)
>>>>>>> 73a22d491c063849a58ac9d3bd9d22a961f91bcb
