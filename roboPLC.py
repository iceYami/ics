def s7_upload_program(target_ip, block_type, block_num):
    """
    Upload program block from PLC
    block_type: 'OB' (Organization Block), 'FC' (Function), 'FB' (Function Block), 'DB' (Data Block)
    """
    import snap7

    plc = snap7.client.Client()
    plc.connect(target_ip, 0, 1)

    # Get block info
    block_info = plc.get_block_info(block_type, block_num)

    # Upload block
    block_data = plc.upload(block_type, block_num)

    plc.disconnect()

    # Save to file
    filename = f"{block_type}{block_num}.mc7"
    with open(filename, 'wb') as f:
        f.write(block_data)

    return block_data

# Usage: s7_upload_program('192.168.1.100', 'OB', 1)
