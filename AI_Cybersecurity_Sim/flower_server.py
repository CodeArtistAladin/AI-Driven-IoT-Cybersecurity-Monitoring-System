import flwr as fl

# Define server strategy
strategy = fl.server.strategy.FedAvg(
    fraction_fit=1.0,
    fraction_evaluate=1.0,
    min_fit_clients=3,
    min_evaluate_clients=3,
    min_available_clients=3,
)

if __name__ == "__main__":
    print("🌐 Starting Flower Federated Server...")
    fl.server.start_server(
        server_address="localhost:8085",
        config=fl.server.ServerConfig(num_rounds=3),
        strategy=strategy,
    )
