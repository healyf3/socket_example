import time
import sys
import socket
import selectors
import types

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

sel = selectors.DefaultSelector()
messages = [b"Message 1 from client.", b"Message 2 from client."]

def start_connections(host, port):
    server_addr = (host, port)
    connid = 2
    print(f"Starting connection {connid} to {server_addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    events = selectors.EVENT_READ
    data = types.SimpleNamespace(
        connid=connid,
        msg_total=sum(len(m) for m in messages),
        recv_total=0,
        messages=messages.copy(),
        outb=b"",
    )
    sel.register(sock, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
            print(f"Received {recv_data!r} from connection {data.connid}")
            data.recv_total += len(recv_data)
        else:
            print(f"Closing connection {data.connid}")
        if not recv_data or data.recv_total == data.msg_total:
            pass
            #print(f"Closing connection {data.connid}")
            #sel.unregister(sock)
            #sock.close()


start_connections(HOST, PORT)
while 1:
    events = sel.select(timeout=None)
    for key, mask in events:
        service_connection(key, mask)
