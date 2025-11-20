import tensorflow as tf
import numpy as np
import time
import random

# Load your TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path="basic_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("✅ Model loaded successfully. Starting live simulation...\n")

# Simulate real-time sensor readings
for i in range(20):  # simulate 20 readings
    # Simulate a fake sensor value between 0.1 and 1.0
    sensor_value = round(random.uniform(0.1, 1.0), 2)
    
    # Prepare the input
    input_data = np.array([[sensor_value]], dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])[0][0]
    
    print(f"📡 Sensor Reading: {sensor_value} → AI Prediction: {round(output, 3)}")
    
    # Wait a bit before next reading
    time.sleep(1)

print("\n✅ Simulation finished successfully.")
