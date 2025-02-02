import socket
import threading
import asyncio
import aioquic
from aioquic.asyncio import QuicConnectionProtocol, serve
from aioquic.quic.configuration import QuicConfiguration

TCP_PORT = 5001
UDP_PORT = 5002
QUIC_PORT = 5003
SERVER_IP = "0.0.0.0"

# TCP Server
def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, TCP_PORT))
    server.listen(5)
    print(f"TCP Server listening on {SERVER_IP}:{TCP_PORT}")

    conn, addr = server.accept()
    print(f"TCP Connection established with {addr}")

    with open("received_file_tcp.txt", "wb") as f:
        while data := conn.recv(1024):
            f.write(data)

    conn.close()
    server.close()
    print("TCP File received successfully.")

# UDP Server
def udp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((SERVER_IP, UDP_PORT))
    print(f"UDP Server listening on {SERVER_IP}:{UDP_PORT}")

    with open("received_file_udp.txt", "wb") as f:
        while True:
            data, addr = server.recvfrom(1024)
            if not data:
                break
            f.write(data)

    server.close()
    print("UDP File received successfully.")

# QUIC Server
class SimpleQuicServerProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

async def quic_server():
    config = QuicConfiguration(is_client=False)
    server = await serve(SERVER_IP, QUIC_PORT, configuration=config, create_protocol=SimpleQuicServerProtocol)
    
    # Keep the server running indefinitely
    try:
        print('quic server running')
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("QUIC Server shutting down...")

    
    
# Start all servers
threading.Thread(target=tcp_server).start()
threading.Thread(target=udp_server).start()
asyncio.run(quic_server())
