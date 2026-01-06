def s7_read_area(target_ip, area, db_number, start, count):
    """
    Read arbitrary memory area from S7 PLC
    area: 0x84 (DB), 0x81 (I), 0x82 (Q), 0x83 (M)
    """
    # Implementation using python-snap7 library
    import snap7
    from snap7.util import *

    plc = snap7.client.Client()
    plc.connect(target_ip, 0, 1)  # IP, rack, slot

    if area == 0x84:  # DB
        data = plc.db_read(db_number, start, count)
    elif area == 0x81:  # Input
        data = plc.read_area(snap7.types.Areas.PE, 0, start, count)
    elif area == 0x82:  # Output
        data = plc.read_area(snap7.types.Areas.PA, 0, start, count)
    elif area == 0x83:  # Marker
        data = plc.read_area(snap7.types.Areas.MK, 0, start, count)

    plc.disconnect()
    return data

# Example: Read DB1, starting at byte 0, read 100 bytes
data = s7_read_area('192.168.1.100', 0x84, 1, 0, 100)
