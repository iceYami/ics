# plc_firmware_downloader.py - Download firmware from PLC web interface
import requests
from requests.auth import HTTPBasicAuth

class PLCFirmwareDownloader:
    def __init__(self, plc_ip, username="admin", password="admin"):
        self.base_url = f"http://{plc_ip}"
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()

    def download_siemens_s7(self):
        """Download firmware from Siemens S7-1200 web interface"""
        # Navigate to firmware backup page
        backup_url = f"{self.base_url}/Firmware/Backup.html"

        # Trigger backup generation
        response = self.session.post(
            f"{self.base_url}/api/firmware/backup",
            auth=self.auth
        )

        if response.status_code == 200:
            backup_id = response.json()['backup_id']

            # Download generated backup
            download_url = f"{self.base_url}/api/firmware/download/{backup_id}"
            firmware = self.session.get(download_url, auth=self.auth)

            with open('s7_firmware.bin', 'wb') as f:
                f.write(firmware.content)

            print(f"[+] Downloaded {len(firmware.content)} bytes")
            return firmware.content

    def download_schneider_m340(self):
        """Schneider Modicon M340 firmware extraction"""
        # Many Schneider PLCs expose firmware via FTP
        import ftplib

        ftp = ftplib.FTP(self.base_url.replace('http://', ''))
        ftp.login(user='USER', passwd='USER')  # Default Schneider creds

        # List files
        files = ftp.nlst()
        print(f"[+] FTP files: {files}")

        # Download firmware
        with open('m340_firmware.bin', 'wb') as f:
            ftp.retrbinary('RETR firmware.bin', f.write)

        ftp.quit()

# Usage
downloader = PLCFirmwareDownloader("192.168.1.10")
downloader.download_siemens_s7()
