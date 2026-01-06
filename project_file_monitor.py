# project_file_monitor.py - Detect trojanized project files
import hashlib
import os

class ProjectFileMonitor:
    def __init__(self):
        self.baseline_hashes = {}

    def baseline_project(self, project_path):
        """
        Create cryptographic baseline of known-good project
        """
        file_hash = hashlib.sha256(open(project_path, 'rb').read()).hexdigest()
        self.baseline_hashes[project_path] = file_hash
        print(f"[+] Baseline created: {project_path} - {file_hash}")

    def verify_project(self, project_path):
        """
        Verify project hasn't been modified
        """
        current_hash = hashlib.sha256(open(project_path, 'rb').read()).hexdigest()

        if project_path in self.baseline_hashes:
            if current_hash != self.baseline_hashes[project_path]:
                print(f"[!] ALERT: Project file modified: {project_path}")
                print(f"[!] Expected: {self.baseline_hashes[project_path]}")
                print(f"[!] Current:  {current_hash}")
                return False

        return True

# Deploy on file server hosting project files
monitor = ProjectFileMonitor()
monitor.baseline_project(r"\\fileserver\projects\PlantControl.ap17")
