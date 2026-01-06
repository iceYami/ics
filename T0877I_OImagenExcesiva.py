# Zeek script for anomalous Modbus reads
@load base/frameworks/notice

global modbus_read_threshold = 100;  # Reads per hour
global modbus_read_count: table[addr] of count;

event modbus_message(c: connection, headers: ModbusHeaders, is_orig: bool) {
    if (headers$function_code in [1, 2, 3, 4]) {  # Read functions
        if (c$id$orig_h !in modbus_read_count)
            modbus_read_count[c$id$orig_h] = 0;

        ++modbus_read_count[c$id$orig_h];

        if (modbus_read_count[c$id$orig_h] > modbus_read_threshold)
            NOTICE([$note=ModbusExcessiveRead,
                    $msg=fmt("Excessive Modbus reads from %s", c$id$orig_h),
                    $conn=c]);
    }
}
