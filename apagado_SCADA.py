#!/usr/bin/env python3
"""
Multi-protocol ICS device enumeration and testing
WARNING: Can disrupt operations - use only in authorized testing
"""

import socket
import struct
import sys

def test_modbus(ip, port=502):
    """Test Modbus connectivity"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))

        # Read Device Identification (FC 0x2B/0x0E)
        trans_id = b'\x00\x01'
        proto_id = b'\x00\x00'
        length = b'\x00\x05'
        unit_id = b'\x01'
        func_code = b'\x2B'
        mei_type = b'\x0E'
        read_device_id = b'\x01\x00'

        request = trans_id + proto_id + length + unit_id + func_code + mei_type + read_device_id

        sock.send(request)
        response = sock.recv(1024)

        if len(response) > 9:
            print(f"[+] {ip}:502 - Modbus ACTIVE")
            return True

    except:
        pass
    finally:
        sock.close()

    return False

def test_s7(ip, port=102):
    """Test Siemens S7 connectivity"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))

        # COTP Connection Request
        cotp_cr = bytes.fromhex('0300001611e0000000010000c00100c10200c20200')
        sock.send(cotp_cr)
        response = sock.recv(1024)

        if len(response) > 0 and response[5:6] == b'\xd0':
            print(f"[+] {ip}:102 - Siemens S7 ACTIVE")
            return True

    except:
        pass
    finally:
        sock.close()

    return False

def test_enip(ip, port=44818):
    """Test Ethernet/IP connectivity"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))

        # ListIdentity command
        command = struct.pack('<H', 0x0063)
        length = struct.pack('<H', 0)
        session = b'\x00' * 4
        status = b'\x00' * 4
        context = b'\x00' * 8
        options = b'\x00' * 4

        request = command + length + session + status + context + options

        sock.send(request)
        response = sock.recv(1024)

        if len(response) > 24:
            print(f"[+] {ip}:44818 - Ethernet/IP ACTIVE")
            return True

    except:
        pass
    finally:
        sock.close()

    return False

def scan_network(network):
    """Scan network for ICS devices"""
    import ipaddress

    net = ipaddress.IPv4Network(network, strict=False)

    for ip in net.hosts():
        ip_str = str(ip)
        test_modbus(ip_str)
        test_s7(ip_str)
        test_enip(ip_str)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <network_cidr>")
        sys.exit(1)

    scan_network(sys.argv[1])
