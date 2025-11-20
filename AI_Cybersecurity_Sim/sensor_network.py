<<<<<<< HEAD
import paho.mqtt.client as mqtt
import random
import time
import json

BROKER = "localhost"
TOPIC = "iot/network"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

print("🌐 Network traffic sensor started publishing...")

while True:
    # Normal packet rate
    packets_per_sec = random.randint(100, 300)

    # Simulated DDoS or attack
    if random.random() < 0.1:
        packets_per_sec = random.randint(800, 1500)

    payload = {"sensor": "network", "value": packets_per_sec}
    client.publish(TOPIC, json.dumps(payload))
    print(f"Sent -> {payload}")
    time.sleep(2)
=======
import paho.mqtt.client as mqtt
import random
import time
import json

BROKER = "localhost"
TOPIC = "iot/network"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

print("🌐 Network traffic sensor started publishing...")

while True:
    # Normal packet rate
    packets_per_sec = random.randint(100, 300)

    # Simulated DDoS or attack
    if random.random() < 0.1:
        packets_per_sec = random.randint(800, 1500)

    payload = {"sensor": "network", "value": packets_per_sec}
    client.publish(TOPIC, json.dumps(payload))
    print(f"Sent -> {payload}")
    time.sleep(2)
>>>>>>> 73a22d491c063849a58ac9d3bd9d22a961f91bcb
