event modbus_write_single_register_request(c: connection, headers: ModbusHeaders, address: count, value: count)
{
    print fmt("Modbus Write: %s wrote %d to register %d", c$id$orig_h, value, address);

    # Alert on writes to critical registers
    if (address in critical_registers)
        NOTICE([$note=ModbusCriticalWrite,
                $msg=fmt("Write to critical register %d", address),
                $conn=c]);
}
