import socket
import struct
import random

def fuzz_modbus(target_ip, target_port=502, iterations=1000):
    """
    Fuzzes Modbus TCP implementation by sending malformed packets
    """

    valid_function_codes = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x0F, 0x10]

    for i in range(iterations):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        try:
            sock.connect((target_ip, target_port))

            # Fuzzing strategies
            strategy = random.choice(['valid_fc_invalid_data', 'invalid_fc', 'malformed_header', 'oversized'])

            if strategy == 'valid_fc_invalid_data':
                # Valid function code, random data
                fc = random.choice(valid_function_codes)
                data = bytes([random.randint(0, 255) for _ in range(random.randint(0, 255))])

            elif strategy == 'invalid_fc':
                # Invalid/reserved function codes
                fc = random.choice([x for x in range(256) if x not in valid_function_codes])
                data = b'\x00\x00\x00\x01'

            elif strategy == 'malformed_header':
                # Invalid MBAP header
                packet = bytes([random.randint(0, 255) for _ in range(random.randint(1, 260))])
                sock.send(packet)
                continue

            elif strategy == 'oversized':
                # Excessively large data
                fc = random.choice(valid_function_codes)
                data = bytes([0x00] * random.randint(256, 4096))

            # Build packet
            trans_id = random.randint(0, 65535)
            proto_id = 0x0000
            length = len(data) + 2
            unit_id = random.randint(0, 255)

            packet = struct.pack('>HHHBB', trans_id, proto_id, length, unit_id, fc) + data

            sock.send(packet)
            response = sock.recv(1024)

            print(f"[{i}] Strategy: {strategy}, FC: {fc:02X}, Response: {len(response)} bytes")

        except socket.timeout:
            print(f"[{i}] Timeout - possible DoS")
        except ConnectionRefusedError:
            print(f"[{i}] Connection refused - service down?")
        except Exception as e:
            print(f"[{i}] Error: {e}")
        finally:
            sock.close()

# Usage: fuzz_modbus('192.168.1.100')
