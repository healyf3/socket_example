# echo-client.py

import socket
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    a = s.connect((HOST, PORT))
    #s.sendall(b"Hello, world")
    while(1):
        data = s.recv(1024)
        print(f"Received {data!r}")
        time.sleep(.3)
