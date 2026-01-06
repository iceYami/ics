#!/usr/bin/env python3
import socket
import struct
import sys

def scan_modbus_registers(target, unit_id=1, start=0, end=100):
    """
    Scan Modbus holding registers to identify valid addresses
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    try:
        sock.connect((target, 502))
        print(f"[+] Connected to {target}:502")

        valid_registers = []

        for addr in range(start, end):
            trans_id = addr + 1
            proto_id = 0
            length = 6
            func_code = 0x03  # Read Holding Registers
            count = 1

            request = struct.pack('>HHHBBHH', trans_id, proto_id, length, unit_id, func_code, addr, count)

            sock.send(request)
            response = sock.recv(1024)

            if len(response) > 8:
                resp_func = response[7]
                if resp_func == 0x03:  # Successful response
                    value = struct.unpack('>H', response[9:11])[0]
                    valid_registers.append((addr, value))
                    print(f"[+] Register {addr}: {value}")
                elif resp_func == 0x83:  # Exception
                    exception = response[8]
                    if exception == 0x02:  # Illegal address
                        continue

        return valid_registers

    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <target_ip>")
        sys.exit(1)

    scan_modbus_registers(sys.argv[1])
