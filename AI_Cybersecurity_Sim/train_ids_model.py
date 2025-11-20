import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt

# 1️⃣ Simulate IoT data (normal vs attack)
np.random.seed(42)
normal_data = np.random.normal(loc=0.3, scale=0.1, size=(500, 1))
attack_data = np.random.normal(loc=0.8, scale=0.1, size=(500, 1))

X = np.vstack((normal_data, attack_data))
y = np.hstack((np.zeros(500), np.ones(500)))  # 0=Normal, 1=Attack

# Shuffle the data
indices = np.arange(len(X))
np.random.shuffle(indices)
X, y = X[indices], y[indices]

# 2️⃣ Define lightweight model
model = keras.Sequential([
    layers.Dense(8, activation='relu', input_shape=(1,)),
    layers.Dense(4, activation='relu'),
    layers.Dense(1, activation='sigmoid')  # Output: probability of attack
])

# 3️⃣ Compile model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 4️⃣ Train model
history = model.fit(X, y, epochs=20, batch_size=16, validation_split=0.2, verbose=0)

# 5️⃣ Evaluate
loss, accuracy = model.evaluate(X, y, verbose=0)
print(f"✅ IDS Model Trained — Accuracy: {accuracy:.2f}")

# 6️⃣ Save models
model.save("ids_model.h5")

# 7️⃣ Convert to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open("ids_model.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ TensorFlow Lite IDS model saved as ids_model.tflite")

# 8️⃣ Plot training accuracy
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.title("IDS Model Training Performance")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.show()
