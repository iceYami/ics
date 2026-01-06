#!/usr/bin/env python3
"""
Decompile Siemens S7 MC7 bytecode to AWL
MC7 is proprietary bytecode format for S7 PLCs
"""

def decompile_mc7_to_awl(mc7_bytes):
    """
    Basic MC7 decompiler
    """
    awl_code = []
    offset = 0

    while offset < len(mc7_bytes):
        opcode = mc7_bytes[offset]

        # MC7 opcodes (simplified subset)
        if opcode == 0x70:  # A (AND)
            operand_type = mc7_bytes[offset+1]
            if operand_type == 0x81:  # Input
                bit_addr = struct.unpack('>H', mc7_bytes[offset+2:offset+4])[0]
                awl_code.append(f"A     I{bit_addr >> 3}.{bit_addr & 0x07}")
                offset += 4
        
        elif opcode == 0x71:  # AN (AND NOT)
            operand_type = mc7_bytes[offset+1]
            if operand_type == 0x81:
                bit_addr = struct.unpack('>H', mc7_bytes[offset+2:offset+4])[0]
                awl_code.append(f"AN    I{bit_addr >> 3}.{bit_addr & 0x07}")
                offset += 4

        elif opcode == 0x76:  # = (Assignment)
            operand_type = mc7_bytes[offset+1]
            if operand_type == 0x82:  # Output
                bit_addr = struct.unpack('>H', mc7_bytes[offset+2:offset+4])[0]
                awl_code.append(f"=     Q{bit_addr >> 3}.{bit_addr & 0x07}")
                offset += 4

        elif opcode == 0xBE:  # CALL
            block_num = struct.unpack('>H', mc7_bytes[offset+1:offset+3])[0]
            awl_code.append(f"CALL  FB{block_num}")
            offset += 3

        else:
            offset += 1  # Unknown opcode, skip

    return '\n'.join(awl_code)

# Example usage:
# mc7_data = open('OB1.mc7', 'rb').read()
# awl = decompile_mc7_to_awl(mc7_data)
# print(awl)
