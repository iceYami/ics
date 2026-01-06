# firmware_integrity_checker.py - Verify PLC firmware integrity
import hashlib
import snap7

class FirmwareIntegrityChecker:
    def __init__(self, plc_ip):
        self.plc = snap7.client.Client()
        self.plc.connect(plc_ip, 0, 1)

        # Known-good firmware hashes (from vendor)
        self.known_good_hashes = {
            "Siemens S7-1200 FW 4.2": "a1b2c3d4e5f6...",
            "Siemens S7-1500 FW 2.8": "1a2b3c4d5e6f...",
        }

    def calculate_firmware_hash(self):
        """
        Download firmware and calculate hash
        """
        # Upload all blocks
        firmware_parts = []

        for block_type in ['OB', 'FB', 'FC', 'DB']:
            block_list = self.plc.list_blocks_of_type(block_type)
            for block_num in block_list:
                data = self.plc.full_upload(block_type, block_num)
                firmware_parts.append(data)

        # Concatenate and hash
        full_firmware = b''.join(firmware_parts)
        firmware_hash = hashlib.sha256(full_firmware).hexdigest()

        return firmware_hash

    def verify_integrity(self):
        """
        Compare against known-good hash
        """
        current_hash = self.calculate_firmware_hash()

        for fw_version, known_hash in self.known_good_hashes.items():
            if current_hash == known_hash:
                print(f"[+] Firmware integrity verified: {fw_version}")
                return True

        print("[!] ALERT: Firmware hash mismatch - possible tampering!")
        print(f"[!] Current hash: {current_hash}")
        return False

# Usage - run periodically
checker = FirmwareIntegrityChecker("192.168.1.10")
checker.verify_integrity()
