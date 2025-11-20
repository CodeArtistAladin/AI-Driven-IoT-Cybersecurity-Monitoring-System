import tensorflow as tf
import numpy as np

# Step 1: Create fake sensor data (simulating IoT readings)
x_train = np.array([[0.1], [0.2], [0.3], [0.4], [0.5],
                    [0.6], [0.7], [0.8], [0.9], [1.0]])
y_train = np.array([[0.2], [0.4], [0.6], [0.8], [1.0],
                    [1.2], [1.4], [1.6], [1.8], [2.0]])

# Step 2: Build a simple neural network model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(8, input_shape=(1,), activation='relu'),
    tf.keras.layers.Dense(1)
])

# Step 3: Compile and train the model
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=300, verbose=0)

# Step 4: Save normal model
model.save("basic_model.h5")
print("✅ Normal model saved as basic_model.h5")

# Step 5: Convert to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Step 6: Save the TensorFlow Lite model
with open("basic_model.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ TensorFlow Lite model saved as basic_model.tflite")

# Step 7: Test prediction using the Lite model
interpreter = tf.lite.Interpreter(model_path="basic_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Simulate a new input (like from an IoT sensor)
new_input = np.array([[0.75]], dtype=np.float32)
interpreter.set_tensor(input_details[0]['index'], new_input)
interpreter.invoke()
output = interpreter.get_tensor(output_details[0]['index'])
print(f"🔮 Prediction for input {new_input[0][0]} is {output[0][0]}")
