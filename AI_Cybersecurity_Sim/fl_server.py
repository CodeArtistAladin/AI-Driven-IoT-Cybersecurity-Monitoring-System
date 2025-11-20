import flwr as fl

# Simple strategy (FedAvg)
strategy = fl.server.strategy.FedAvg(
    min_fit_clients=2,
    min_available_clients=2,
)

print("🌸 Starting Federated Learning Server...")
fl.server.start_server(server_address="localhost:8085", strategy=strategy)
