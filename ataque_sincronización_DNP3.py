def dnp3_time_sync_attack(outstation_ip):
    """
    Send false time synchronization
    Can cause log tampering, event correlation issues
    """
    from pydnp3 import opendnp3

    # Send time sync with incorrect timestamp
    # (1 year in past or future)

    import datetime
    false_time = datetime.datetime.now() + datetime.timedelta(days=365)

    # Build DNP3 time sync request (Group 50)
    # Send via master

    print(f"[+] False time sent: {false_time}")
    print("[*] RTU logs will have incorrect timestamps")

# dnp3_time_sync_attack('192.168.1.100')
