import snap7

def extract_s7_firmware(plc_ip):
    """
    Extract firmware from Siemens S7 PLC
    """
    plc = snap7.client.Client()
    plc.connect(plc_ip, 0, 1)  # Rack 0, Slot 1

    # Get PLC info (firmware version)
    cpu_info = plc.get_cpu_info()
    print(f"PLC: {cpu_info.ModuleTypeName}")
    print(f"Firmware: {cpu_info.ASName}")

    # Upload all blocks
    block_list = plc.list_blocks()
    for block_type in ['OB', 'FB', 'FC', 'DB']:
        for block_num in block_list:
            try:
                block_data = plc.upload(block_type, block_num)
                with open(f"{block_type}{block_num}.mc7", "wb") as f:
                    f.write(block_data)
                print(f"[+] Extracted {block_type}{block_num}")
            except:
                pass

    plc.disconnect()

# Usage
extract_s7_firmware('192.168.1.100')
