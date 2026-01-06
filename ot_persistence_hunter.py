# ot_persistence_hunter.py - Detect persistence mechanisms
class OTPersistenceHunter:
    def __init__(self):
        self.findings = []

    def scan_plc_firmware_integrity(self, plc_ip):
        """
        Verify PLC firmware hasn't been modified
        """
        from snap7 import client
        plc = client.Client()
        plc.connect(plc_ip, 0, 1)

        # Calculate firmware hash
        firmware = plc.full_upload(snap7.types.S7AreaFirmware, 0)
        current_hash = hashlib.sha256(firmware).hexdigest()

        # Compare to known-good hash (from vendor)
        known_good_hash = "a1b2c3..."  # From Siemens database

        if current_hash != known_good_hash:
            self.findings.append(f"ALERT: PLC {plc_ip} firmware modified!")
            return False

        return True

    def check_scheduled_tasks(self, scada_server):
        """
        Enumerate scheduled tasks on SCADA servers
        Look for suspicious tasks
        """
        import subprocess
        output = subprocess.check_output(f'schtasks /query /s {scada_server} /fo csv')

        suspicious_indicators = [
            'powershell.exe -enc',  # Encoded PS commands
            'SYSTEM',  # Running as SYSTEM (unusual for SCADA tasks)
            '02:00',  # Maintenance window (common persistence time)
        ]

        for line in output.decode().split('\n'):
            if any(indicator in line for indicator in suspicious_indicators):
                self.findings.append(f"Suspicious task: {line}")

    def detect_covert_channels(self, pcap_file):
        """
        Analyze Modbus traffic for covert channels
        Look for abnormal register access patterns
        """
        from scapy.all import rdpcap

        packets = rdpcap(pcap_file)

        # Baseline: Normal Modbus register access (registers 0-500)
        # Suspicious: Access to high register numbers (1000+)

        suspicious_registers = []
        for pkt in packets:
            if self.is_modbus_packet(pkt):
                register = self.extract_register_address(pkt)
                if register > 500:
                    suspicious_registers.append(register)

        if suspicious_registers:
            self.findings.append(f"Covert channel detected: Registers {suspicious_registers}")

# Usage
hunter = OTPersistenceHunter()
hunter.scan_plc_firmware_integrity("192.168.1.10")
hunter.check_scheduled_tasks("scada-server-01")
hunter.detect_covert_channels("modbus_traffic.pcap")
