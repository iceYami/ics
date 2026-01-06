import socket
import struct

class ModbusTCP:
    def __init__(self, host, port=502):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.transaction_id = 0

    def connect(self):
        self.sock.connect((self.host, self.port))

    def _build_request(self, unit_id, function_code, data):
        self.transaction_id += 1
        protocol_id = 0
        length = len(data) + 2  # unit_id + function_code + data

        header = struct.pack('>HHHB',
                           self.transaction_id,
                           protocol_id,
                           length,
                           unit_id)
        return header + struct.pack('B', function_code) + data

    def read_holding_registers(self, unit_id, start_addr, count):
        data = struct.pack('>HH', start_addr, count)
        request = self._build_request(unit_id, 0x03, data)

        self.sock.send(request)
        response = self.sock.recv(1024)

        # Parse response
        trans_id, proto_id, length, unit, func_code, byte_count = struct.unpack('>HHHBBB', response[:9])

        if func_code == 0x03:
            registers = []
            for i in range(byte_count // 2):
                reg_value = struct.unpack('>H', response[9 + i*2:11 + i*2])[0]
                registers.append(reg_value)
            return registers
        elif func_code == 0x83:  # Exception
            exception_code = struct.unpack('B', response[9:10])[0]
            raise Exception(f"Modbus Exception: {exception_code}")

    def write_single_register(self, unit_id, address, value):
        data = struct.pack('>HH', address, value)
        request = self._build_request(unit_id, 0x06, data)

        self.sock.send(request)
        response = self.sock.recv(1024)
        return response

# Usage
mb = ModbusTCP('192.168.1.100')
mb.connect()
registers = mb.read_holding_registers(unit_id=1, start_addr=0, count=10)
print(f"Registers: {registers}")
