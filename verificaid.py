import hashlib

def verify_plc_integrity(plc_ip, golden_hash):
    """
    Compare PLC firmware hash with known-good hash
    """
    plc = snap7.client.Client()
    plc.connect(plc_ip, 0, 1)

    # Upload OB1 (main logic)
    ob1 = plc.upload('OB', 1)

    current_hash = hashlib.sha256(ob1).hexdigest()
    print(f"Current OB1 hash: {current_hash}")
    print(f"Golden OB1 hash:  {golden_hash}")

    if current_hash == golden_hash:
        print("[+] Integrity check PASSED")
    else:
        print("[!] ALERT: OB1 has been modified!")

    plc.disconnect()

# Baseline hash from known-good configuration
golden_hash = "abc123def456..."
verify_plc_integrity('192.168.1.100', golden_hash)
