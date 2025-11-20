<<<<<<< HEAD
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
=======
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
>>>>>>> 73a22d491c063849a58ac9d3bd9d22a961f91bcb
