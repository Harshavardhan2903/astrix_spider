import socket
import asyncio
import aioquic
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio import connect
import speedtest
import psutil
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle


SERVER_IP = "127.0.0.1"
TCP_PORT = 5001
UDP_PORT = 5002
QUIC_PORT = 5003


def get_network_conditions():
    st = speedtest.Speedtest()
    st.get_best_server()
    
    download_speed = st.download() / 1e6  # Mbps
    upload_speed = st.upload() / 1e6  # Mbps
    latency = st.results.ping  # ms
    packet_loss = psutil.net_io_counters().dropin  # Dropped packets
    print(latency,download_speed,packet_loss)

    return {"latency": latency, "bandwidth": download_speed, "packet_loss": packet_loss}


# TCP File Transfer
def send_tcp(data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, TCP_PORT))
    client.sendall(data)
    client.close()

# UDP File Transfer
def send_udp(data):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(data, (SERVER_IP, UDP_PORT))
    client.close()

# QUIC File Transfer
async def send_quic(data):
    config = QuicConfiguration(is_client=True)
    async with connect(SERVER_IP, QUIC_PORT, configuration=config) as connection:
        await connection.send(data)

#asyncio.run(send_quic(b"Hello from QUIC!"))

def select_protocol():
    with open("protocol_selector.pkl", "rb") as f:
        model = pickle.load(f)

    conditions = get_network_conditions()
    best_protocol = model.predict([[conditions["latency"], conditions["bandwidth"], conditions["packet_loss"]]])
    #print("the protocol selected is ",best_protocol)
    return best_protocol[0]

    print(f"AI Selected Protocol: {select_protocol()}")

# Adaptive File Transfer
def adaptive_file_transfer(file_path):
    with open(file_path, "rb") as f:
        while chunk := f.read(1024):
            best_protocol = select_protocol()
            print(f"Sending via {best_protocol}...")

            if best_protocol == "TCP":
                send_tcp(chunk)
            elif best_protocol == "UDP":
                send_udp(chunk)
            elif best_protocol == "QUIC":
                asyncio.run(send_quic(chunk))

adaptive_file_transfer("message.txt")
