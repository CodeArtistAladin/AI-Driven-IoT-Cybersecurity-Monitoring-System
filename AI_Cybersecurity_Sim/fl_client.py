<<<<<<< HEAD
import flwr as fl
import tensorflow as tf
from tensorflow import keras
import numpy as np

# Simulated dataset (each client gets different random data)
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train, y_train = x_train / 255.0, y_train
x_test, y_test = x_test / 255.0, y_test

# Take small random portion to simulate local device data
idx = np.random.choice(len(x_train), 2000, replace=False)
x_train, y_train = x_train[idx], y_train[idx]

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

class FlowerClient(fl.client.NumPyClient):
    def get_parameters(self, config):
        return model.get_weights()

    def fit(self, parameters, config):
        model.set_weights(parameters)
        model.fit(x_train, y_train, epochs=1, batch_size=32, verbose=0)
        return model.get_weights(), len(x_train), {}

    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        loss, acc = model.evaluate(x_test, y_test, verbose=0)
        return loss, len(x_test), {"accuracy": acc}

fl.client.start_numpy_client(server_address="localhost:8085", client=FlowerClient())
=======
import flwr as fl
import tensorflow as tf
from tensorflow import keras
import numpy as np

# Simulated dataset (each client gets different random data)
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train, y_train = x_train / 255.0, y_train
x_test, y_test = x_test / 255.0, y_test

# Take small random portion to simulate local device data
idx = np.random.choice(len(x_train), 2000, replace=False)
x_train, y_train = x_train[idx], y_train[idx]

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

class FlowerClient(fl.client.NumPyClient):
    def get_parameters(self, config):
        return model.get_weights()

    def fit(self, parameters, config):
        model.set_weights(parameters)
        model.fit(x_train, y_train, epochs=1, batch_size=32, verbose=0)
        return model.get_weights(), len(x_train), {}

    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        loss, acc = model.evaluate(x_test, y_test, verbose=0)
        return loss, len(x_test), {"accuracy": acc}

fl.client.start_numpy_client(server_address="localhost:8085", client=FlowerClient())
>>>>>>> 73a22d491c063849a58ac9d3bd9d22a961f91bcb
