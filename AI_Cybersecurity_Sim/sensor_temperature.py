import paho.mqtt.client as mqtt
import random
import time
import json

BROKER = "localhost"
TOPIC = "iot/temperature"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

print("🌡️ Temperature sensor started publishing...")

while True:
    # Normal readings
    temp = round(random.uniform(22.0, 28.0), 2)

    # Random anomaly (simulate overheating)
    if random.random() < 0.1:  # 10% chance
        temp += random.uniform(5, 15)

    payload = {"sensor": "temperature", "value": temp}
    client.publish(TOPIC, json.dumps(payload))
    print(f"Sent -> {payload}")
    time.sleep(2)
