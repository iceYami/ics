#!/usr/bin/env python3
"""
RF monitoring for WirelessHART network
Alerts on unauthorized devices or jamming
"""

from killerbee import KillerBee
import hashlib

authorized_devices = [
    "00:12:4b:00:01:23:45:67",
    "00:12:4b:00:89:ab:cd:ef"
]

def monitor_wireless_network(channel=11):
    kb = KillerBee()
    kb.set_channel(channel)

    print(f"[*] Monitoring channel {channel} for unauthorized devices...")

    while True:
        packet = kb.pnext()
        if packet:
            # Extract source address
            src_addr = extract_src_address(packet)

            if src_addr not in authorized_devices:
                print(f"[!] ALERT: Unauthorized device detected: {src_addr}")
                # Send alert (email, SIEM, etc.)

            # Detect jamming (excessive corrupted packets)
            if is_corrupted(packet):
                print(f"[!] ALERT: Potential jamming detected")

def extract_src_address(packet):
    # Parse IEEE 802.15.4 packet
    # Source address at offset 7-14 (for long addressing)
    return packet[7:15].hex()

def is_corrupted(packet):
    # Check FCS (Frame Check Sequence)
    # Return True if invalid
    return False  # Simplified

# Usage: monitor_wireless_network()
