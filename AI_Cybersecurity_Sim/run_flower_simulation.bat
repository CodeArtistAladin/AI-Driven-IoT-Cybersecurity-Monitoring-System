start cmd /k "python fl_server.py"
timeout /t 5
start cmd /k "python fl_client.py"
timeout /t 2
start cmd /k "python fl_client.py"
timeout /t 2
start cmd /k "python fl_client.py"
