#!/usr/bin/env python3
# modbus_register_scanner.py

import snap7
from pymodbus.client import ModbusTcpClient

def scan_modbus_registers(ip, unit_id=1, start=0, end=1000):
    client = ModbusTcpClient(ip, port=502)
    client.connect()

    valid_registers = []

    for addr in range(start, end):
        try:
            result = client.read_holding_registers(addr, 1, unit=unit_id)
            if not result.isError():
                value = result.registers[0]
                valid_registers.append({"address": addr, "value": value})
                print(f"[+] Register {addr}: {value}")
        except:
            pass

    client.close()
    return valid_registers

# Execute
registers = scan_modbus_registers('10.10.10.10')

# Save to JSON
import json
with open("modbus_register_map.json", "w") as f:
    json.dump(registers, f, indent=2)
