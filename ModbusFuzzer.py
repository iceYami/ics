#!/usr/bin/env python3
import socket
import struct
import random
import time

class ModbusFuzzer:
    def __init__(self, target_ip, port=502):
        self.target_ip = target_ip
        self.port = port
        self.iteration = 0
        self.crashes = []

    def generate_fuzzed_packet(self):
        """
        Generate fuzzed Modbus packet
        """
        strategies = [
            self.fuzz_header,
            self.fuzz_function_code,
            self.fuzz_data_length,
            self.fuzz_random_bytes,
            self.fuzz_valid_packet_mutated
        ]

        fuzzer = random.choice(strategies)
        return fuzzer()

    def fuzz_header(self):
        """
        Fuzz MBAP header fields
        """
        trans_id = struct.pack('>H', random.randint(0, 65535))
        proto_id = struct.pack('>H', random.randint(0, 65535))  # Should be 0x0000
        length = struct.pack('>H', random.randint(0, 500))
        unit_id = bytes([random.randint(0, 255)])
        func_code = bytes([random.randint(0, 255)])
        data = bytes([random.randint(0, 255) for _ in range(random.randint(0, 250))])

        return trans_id + proto_id + length + unit_id + func_code + data

    def fuzz_function_code(self):
        """
        Send invalid/reserved function codes
        """
        trans_id = b'\x00\x01'
        proto_id = b'\x00\x00'
        unit_id = b'\x01'

        # Reserved/invalid function codes
        invalid_fcs = [0x00, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x18, 0x80-0xFF]
        func_code = bytes([random.choice(invalid_fcs)])

        data = bytes([random.randint(0, 255) for _ in range(random.randint(0, 10))])
        length = struct.pack('>H', len(unit_id + func_code + data))

        return trans_id + proto_id + length + unit_id + func_code + data

    def fuzz_data_length(self):
        """
        Send mismatched length fields
        """
        trans_id = b'\x00\x01'
        proto_id = b'\x00\x00'
        unit_id = b'\x01'
        func_code = b'\x03'  # Read Holding Registers

        # Create large data buffer
        data = bytes([0x00] * random.randint(300, 5000))

        # Incorrect length field
        length = struct.pack('>H', random.randint(0, 100))

        return trans_id + proto_id + length + unit_id + func_code + data

    def fuzz_random_bytes(self):
        """
        Completely random packet
        """
        return bytes([random.randint(0, 255) for _ in range(random.randint(1, 500))])

    def fuzz_valid_packet_mutated(self):
        """
        Start with valid packet, mutate bytes
        """
        # Valid Read Holding Registers request
        packet = bytearray(b'\x00\x01\x00\x00\x00\x06\x01\x03\x00\x00\x00\x0A')

        # Mutate 1-3 bytes
        for _ in range(random.randint(1, 3)):
            pos = random.randint(0, len(packet) - 1)
            packet[pos] = random.randint(0, 255)

        return bytes(packet)

    def send_packet(self, packet):
        """
        Send fuzzed packet and check for crash
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.target_ip, self.port))

            sock.send(packet)
            response = sock.recv(1024)

            sock.close()
            return True, response

        except socket.timeout:
            print(f"[!] Iteration {self.iteration}: Timeout (possible hang)")
            return False, None

        except ConnectionRefusedError:
            print(f"[!] Iteration {self.iteration}: Connection refused (possible crash)")
            self.crashes.append({
                'iteration': self.iteration,
                'packet': packet.hex(),
                'error': 'Connection Refused'
            })
            return False, None

        except Exception as e:
            print(f"[!] Iteration {self.iteration}: {e}")
            return False, None

    def run(self, iterations=1000):
        """
        Run fuzzing campaign
        """
        print(f"[*] Starting Modbus fuzzer against {self.target_ip}:{self.port}")
        print(f"[*] Iterations: {iterations}")

        for i in range(iterations):
            self.iteration = i

            packet = self.generate_fuzzed_packet()
            success, response = self.send_packet(packet)

            if success:
                print(f"[{i}] Sent {len(packet)} bytes, received {len(response)} bytes")
            else:
                # Wait for device to recover
                time.sleep(5)

            # Rate limiting
            time.sleep(0.1)

        print(f"\n[*] Fuzzing complete")
        print(f"[*] Potential crashes: {len(self.crashes)}")

        # Save crash logs
        if self.crashes:
            with open("modbus_crashes.log", "w") as f:
                for crash in self.crashes:
                    f.write(f"Iteration: {crash['iteration']}\n")
                    f.write(f"Packet: {crash['packet']}\n")
                    f.write(f"Error: {crash['error']}\n\n")

# Usage
# fuzzer = ModbusFuzzer('192.168.1.100')
# fuzzer.run(iterations=1000)
