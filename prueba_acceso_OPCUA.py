async def test_anonymous_access(endpoint_url):
    """
    Test if server allows anonymous access
    """
    client = Client(endpoint_url)

    # Try security mode None
    client.set_security_string("None")

    try:
        await client.connect()
        print("[+] Anonymous access allowed!")

        # Try reading sensitive data
        root = client.get_root_node()
        objects = await root.get_child(["0:Objects"])
        await browse_node(objects)

        await client.disconnect()
        return True

    except Exception as e:
        print(f"[-] Anonymous access denied: {e}")
        return False
