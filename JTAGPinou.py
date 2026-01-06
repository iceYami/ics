#jtag_scanner.py - Automated JTAG pinout detection
import itertools

def jtag_scan(pins):
    """
    Try all pin combinations to identify TDI, TDO, TCK, TMS
    Based on IDCODE response pattern
    """
    for combo in itertools.permutations(pins, 4):
        tdi, tdo, tck, tms = combo
        # Set up GPIO pins
        setup_gpio(tck, tms, tdi, tdo)

        # Send IDCODE instruction (0b00100)
        send_jtag_instruction(0x02, tck, tms, tdi)

        # Shift out 32 bits
        idcode = shift_data_out(32, tck, tdo)

        # Check if valid IDCODE (LSB must be 1, standard mandates)
        if idcode & 0x1 and idcode != 0xFFFFFFFF:
            print(f"[+] JTAG found: TCK={tck}, TMS={tms}, TDI={tdi}, TDO={tdo}")
            print(f"[+] IDCODE: 0x{idcode:08x}")
            return combo

    return None
