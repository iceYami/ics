class S7commMITMProxy:
    def inspect_s7comm(self, data, direction):
        """
        Inspect S7comm traffic
        """
        if len(data) < 10:
            return data

        # Check for TPKT header
        if data[0:2] != b'\x03\x00':
            return data

        tpkt_length = struct.unpack('>H', data[2:4])[0]

        # Check for COTP Data packet (0xF0)
        if len(data) > 5 and data[5] == 0xF0:
            # S7comm header starts at offset 7
            protocol_id = data[7]
            rosctr = data[8]  # Message type

            if protocol_id == 0x32:  # S7comm
                print(f"[{direction}] S7comm ROSCTR: 0x{rosctr:02X}")

                # Attack: Intercept program download
                if rosctr == 0x01:  # Job request
                    func_code = data[17] if len(data) > 17 else 0
                    print(f"    Function: 0x{func_code:02X}")

                    # FC 0x1D: Start Upload (program extraction)
                    if func_code == 0x1D:
                        print("    [!] DETECTED: Program upload in progress")

                    # FC 0x28: PLC Control (start/stop)
                    if func_code == 0x28:
                        print("    [!] DETECTED: PLC control command")

                        # Could block PLC STOP command here
                        # Or modify to force STOP

        return data

# Integrate into proxy similar to Modbus example
