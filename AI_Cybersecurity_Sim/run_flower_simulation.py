import os
import subprocess
import time

# Start server
server = subprocess.Popen(["python", "flower_server.py"])
time.sleep(3)  # Wait a bit for server to start

# Start 3 simulated clients
clients = []
for i in range(3):
    clients.append(subprocess.Popen(["python", "flower_client.py"]))
    time.sleep(1)

# Wait for all processes to complete
for c in clients:
    c.wait()

server.terminate()
print("\n✅ Federated learning simulation completed.\n")
