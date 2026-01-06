# spi_dumper.py - Low-level SPI flash reading
import spidev

class SPIFlashDumper:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0

    def read_jedec_id(self):
        """Read manufacturer and device ID"""
        response = self.spi.xfer2([0x9F, 0x00, 0x00, 0x00])
        return response[1:]  # [manufacturer, memory_type, capacity]

    def read_page(self, address):
        """Read 256-byte page"""
        cmd = [0x03,  # READ command
               (address >> 16) & 0xFF,
               (address >> 8) & 0xFF,
               address & 0xFF]
        cmd.extend([0x00] * 256)  # Dummy bytes for read

        response = self.spi.xfer2(cmd)
        return bytes(response[4:])  # Skip command bytes

    def dump_full_chip(self, size_mb, output_file):
        """Dump entire flash chip"""
        total_bytes = size_mb * 1024 * 1024

        with open(output_file, 'wb') as f:
            for addr in range(0, total_bytes, 256):
                page = self.read_page(addr)
                f.write(page)

                if addr % 0x10000 == 0:  # Progress every 64KB
                    print(f"[*] Dumped {addr / total_bytes * 100:.1f}%")

# Usage
dumper = SPIFlashDumper()
jedec = dumper.read_jedec_id()
print(f"[+] Flash ID: {jedec.hex()}")
dumper.dump_full_chip(4, "firmware_dump.bin")  # 4MB chip
