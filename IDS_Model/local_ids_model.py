import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import tensorflow as tf

# Step 1: Simulate sample IoT network data (normal + attack)
data = {
    "packet_size": np.random.randint(20, 1000, 2000),
    "duration": np.random.uniform(0.1, 10, 2000),
    "src_bytes": np.random.randint(0, 5000, 2000),
    "dst_bytes": np.random.randint(0, 5000, 2000),
    "failed_logins": np.random.randint(0, 5, 2000),
    "label": np.random.choice(["normal", "attack"], 2000, p=[0.8, 0.2])
}

df = pd.DataFrame(data)

# Step 2: Preprocess
X = df.drop("label", axis=1)
y = (df["label"] == "attack").astype(int)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 3: Train ML model (Random Forest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 4: Evaluate model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Step 5: Convert trained model into TensorFlow Lite format (for ESP32 later)
# First convert the Random Forest output to TensorFlow model (simplified)
rf_predictions = model.predict_proba(X_train)[:, 1]

tf_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(1,)),
    tf.keras.layers.Dense(8, activation="relu"),
    tf.keras.layers.Dense(4, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

tf_model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
tf_model.fit(rf_predictions.reshape(-1, 1), y_train, epochs=10, verbose=1)

# Convert to TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(tf_model)
tflite_model = converter.convert()

with open("local_ids_model.tflite", "wb") as f:
    f.write(tflite_model)

print("\n✅ Model successfully converted to TensorFlow Lite format: local_ids_model.tflite")
