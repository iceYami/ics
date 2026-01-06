def analyze_plc_logic(awl_code):
    """
    Analyze decompiled ladder logic for attack vectors
    """
    critical_outputs = []
    safety_interlocks = []
    timers = []

    for line in awl_code.split('\n'):
        # Find output assignments (actuators)
        if '= Q' in line:
            output = line.split('Q')[1].strip()
            critical_outputs.append(output)
            print(f"[*] Output: Q{output}")

        # Find safety interlocks (AND NOT conditions)
        if 'AN' in line and ('ESTOP' in line or 'ALARM' in line):
            safety_interlocks.append(line)
            print(f"[!] Safety interlock: {line}")

        # Find timers
        if 'T' in line:
            timers.append(line)

    print(f"\n[*] Found {len(critical_outputs)} outputs")
    print(f"[!] Found {len(safety_interlocks)} safety interlocks")
    print(f"[*] Found {len(timers)} timers")

    return critical_outputs, safety_interlocks, timers
