# asset_inventory.zeek
@load base/frameworks/notice

module AssetInventory;

export {
    redef enum Notice::Type += {
        NewICSDevice
    };

    global ics_devices: set[addr];
}

event modbus_message(c: connection, headers: ModbusHeaders, is_orig: bool) {
    if (c$id$resp_h !in ics_devices) {
        add ics_devices[c$id$resp_h];
        NOTICE([$note=NewICSDevice,
                $msg=fmt("New Modbus device discovered: %s", c$id$resp_h),
                $conn=c]);
    }
}

event zeek_done() {
    print "ICS Devices Discovered:", ics_devices;
}
