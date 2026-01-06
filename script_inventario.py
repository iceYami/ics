#!/usr/bin/env python3
import json
import subprocess
import xmltodict

def nmap_scan_to_inventory(target_network):
    """
    Run Nmap scan and parse to asset inventory
    """
    # Run Nmap with XML output
    cmd = [
        "nmap", "-Pn", "-sT", "-sV",
        "-p", "80,102,502,2222,4840,20000,44818,47808",
        "--script", "banner,ics-detect",
        "-oX", "scan_output.xml",
        target_network
    ]

    subprocess.run(cmd)

    # Parse XML output
    with open("scan_output.xml") as f:
        data = xmltodict.parse(f.read())

    inventory = []

    hosts = data['nmaprun'].get('host', [])
    if not isinstance(hosts, list):
        hosts = [hosts]

    for host in hosts:
        if host.get('status', {}).get('@state') != 'up':
            continue

        asset = {
            "ip_address": host.get('address', {}).get('@addr'),
            "mac_address": None,
            "open_ports": [],
            "protocols": [],
            "device_info": {}
        }

        # Extract MAC if available
        addresses = host.get('address', [])
        if not isinstance(addresses, list):
            addresses = [addresses]

        for addr in addresses:
            if addr.get('@addrtype') == 'mac':
                asset['mac_address'] = addr.get('@addr')
                asset['vendor'] = addr.get('@vendor')

        # Extract ports
        ports = host.get('ports', {}).get('port', [])
        if not isinstance(ports, list):
            ports = [ports]

        for port in ports:
            if port.get('state', {}).get('@state') == 'open':
                port_num = port.get('@portid')
                asset['open_ports'].append(int(port_num))

                # Identify protocol
                if port_num == '502':
                    asset['protocols'].append('Modbus')
                elif port_num == '102':
                    asset['protocols'].append('S7comm')
                elif port_num == '44818':
                    asset['protocols'].append('Ethernet/IP')
                elif port_num == '20000':
                    asset['protocols'].append('DNP3')
                elif port_num == '4840':
                    asset['protocols'].append('OPC UA')

        inventory.append(asset)

    # Save inventory
    with open("asset_inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)

    print(f"[+] Inventory saved: {len(inventory)} devices")
    return inventory

# Usage
nmap_scan_to_inventory("192.168.1.0/24")
