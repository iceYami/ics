def dnp3_reconnaissance(target_rtu):
    """
    Enumerate DNP3 outstation configuration
    Discover available control points, analog inputs, binary inputs
    """
    from pydnp3 import opendnp3, asiodnp3

    manager = asiodnp3.DNP3Manager(1)

    channel = manager.AddTCPClient(
        "recon_channel",
        opendnp3.levels.NORMAL,
        asiopal.ChannelRetry(),
        target_rtu,
        "0.0.0.0",
        20000,
        asiodnp3.LinkConfig(False, False)
    )

    master = channel.AddMaster(
        "recon_master",
        asiodnp3.PrintingSOEHandler(),
        asiodnp3.DefaultMasterApplication(),
        asiodnp3.MasterStackConfig()
    )

    master.Enable()

    # Request all data (Class 0 read)
    # Group 60, Variation 1 = All data
    print(f"[*] Enumerating {target_rtu}...")

    # This triggers read of all points
    # Response will contain:
    # - All binary inputs (circuit breaker status)
    # - All analog inputs (voltage, current, frequency)
    # - All control points (breaker controls)

    # Parse response to build map of RTU
    # (pydnp3 PrintingSOEHandler will display all points)

    print("[*] Enumeration complete")
    print("    Use output to identify critical control points")

# dnp3_reconnaissance('192.168.1.100')
