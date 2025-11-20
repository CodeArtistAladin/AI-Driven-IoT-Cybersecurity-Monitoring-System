import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from tqdm import tqdm

# ----- Step 1: Simulate IoT Device Data -----
def generate_device_data(size=1000, attack_ratio=0.2, random_state=None):
    np.random.seed(random_state)
    data = {
        "packet_size": np.random.randint(20, 1000, size),
        "duration": np.random.uniform(0.1, 10, size),
        "src_bytes": np.random.randint(0, 5000, size),
        "dst_bytes": np.random.randint(0, 5000, size),
        "failed_logins": np.random.randint(0, 5, size),
        "label": np.random.choice(["normal", "attack"], size, p=[1 - attack_ratio, attack_ratio])
    }
    df = pd.DataFrame(data)
    X = df.drop("label", axis=1)
    y = (df["label"] == "attack").astype(int)
    return X, y

# ----- Step 2: Define a Simple Neural Network -----
def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(5,)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# ----- Step 3: Federated Learning Simulation -----
NUM_CLIENTS = 5  # Simulating 5 IoT devices
EPOCHS = 3

# Create local datasets
client_data = [generate_device_data(size=800, random_state=i) for i in range(NUM_CLIENTS)]

# Initialize global model
global_model = create_model()

def federated_average(weights_list):
    """Average weights from all clients"""
    avg_weights = []
    for weights in zip(*weights_list):
        avg_weights.append(np.mean(np.array(weights), axis=0))
    return avg_weights

# ----- Step 4: Start Federated Rounds -----
for round in range(5):  # 5 global rounds
    print(f"\n🌐 Federated Round {round+1}")
    local_weights = []

    for i, (X, y) in enumerate(client_data):
        print(f"Training on client {i+1}...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        local_model = create_model()
        local_model.set_weights(global_model.get_weights())

        local_model.fit(X_train, y_train, epochs=EPOCHS, batch_size=32, verbose=0)
        local_weights.append(local_model.get_weights())

    # Aggregate all clients' model weights
    new_global_weights = federated_average(local_weights)
    global_model.set_weights(new_global_weights)

    # Evaluate global model on one client’s test set (for simplicity)
    X_test_scaled = scaler.transform(X_test)
    y_pred = (global_model.predict(X_test_scaled) > 0.5).astype(int)
    acc = accuracy_score(y_test, y_pred)
    print(f"Global Model Accuracy after round {round+1}: {acc:.4f}")

# Save final global model
global_model.save("federated_global_model.h5")
print("\n✅ Federated Global Model saved as 'federated_global_model.h5'")
