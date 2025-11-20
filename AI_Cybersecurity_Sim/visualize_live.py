import tensorflow as tf
import numpy as np
import random
import time
import matplotlib.pyplot as plt

# Load TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path="basic_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("✅ Model loaded. Starting live visualization...")

# Setup live graph
plt.ion()
fig, ax = plt.subplots()
x_data, sensor_data, prediction_data = [], [], []
line1, = ax.plot(x_data, sensor_data, label='Sensor Value', color='blue')
line2, = ax.plot(x_data, prediction_data, label='AI Prediction', color='red')
ax.set_xlabel("Time (s)")
ax.set_ylabel("Value")
ax.legend()
ax.set_title("Live AI Prediction Visualization")

# Run simulation
for i in range(30):
    sensor_value = round(random.uniform(0.1, 1.0), 2)
    input_data = np.array([[sensor_value]], dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])[0][0]

    # Store data for visualization
    x_data.append(i)
    sensor_data.append(sensor_value)
    prediction_data.append(output)

    # Update graph
    line1.set_xdata(x_data)
    line1.set_ydata(sensor_data)
    line2.set_xdata(x_data)
    line2.set_ydata(prediction_data)
    ax.relim()
    ax.autoscale_view()
    plt.draw()
    plt.pause(0.5)

print("\n✅ Visualization finished.")
plt.ioff()
plt.show()
