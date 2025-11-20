import flwr as fl
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

# Simulated local IoT data
def generate_data(seed):
    np.random.seed(seed)
    x = np.random.rand(200, 10)
    y = (x.sum(axis=1) > 5).astype(int)
    return x, y

x_train, y_train = generate_data(np.random.randint(0, 10000))
x_test, y_test = generate_data(np.random.randint(0, 10000))

# Simple IDS model
def create_model():
    model = models.Sequential([
        layers.Dense(16, activation='relu', input_shape=(10,)),
        layers.Dense(8, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

model = create_model()

# Flower client class
class IoTClient(fl.client.NumPyClient):
    def get_parameters(self, config):
        return model.get_weights()

    def fit(self, parameters, config):
        model.set_weights(parameters)
        model.fit(x_train, y_train, epochs=3, verbose=0)
        return model.get_weights(), len(x_train), {}

    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
        return loss, len(x_test), {"accuracy": accuracy}

if __name__ == "__main__":
    print("🤖 Starting IoT client...")
    fl.client.start_numpy_client(server_address="localhost:8085", client=IoTClient())
