# mqtt_subscriber_ids.py
import paho.mqtt.client as mqtt
import tensorflow as tf
import numpy as np
from datetime import datetime

interpreter = tf.lite.Interpreter(model_path="ids_model.tflite")
interpreter.allocate_tensors()
input_d = interpreter.get_input_details()
output_d = interpreter.get_output_details()

def on_connect(client, userdata, flags, rc):
    print("Connected to broker", rc)
    client.subscribe("home/#")

def on_message(client, userdata, msg):
    try:
        val = float(msg.payload.decode())
    except:
        return
    arr = np.array([[val]], dtype=np.float32)
    interpreter.set_tensor(input_d[0]['index'], arr)
    interpreter.invoke()
    score = float(interpreter.get_tensor(output_d[0]['index'])[0][0])
    pred = 1 if score >= 0.5 else 0
    t = datetime.now().isoformat(sep=' ', timespec='seconds')
    print(f"[{t}] topic={msg.topic} value={val:.3f} → score={score:.3f} → {'ATTACK' if pred else 'normal'}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
