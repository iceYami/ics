description = [[
Enumerates Modbus devices and attempts to read holding registers
]]

author = "ICS Security Researcher"
license = "Same as Nmap"
categories = {"discovery", "intrusive"}

portrule = shortport.port_or_service(502, "modbus", "tcp")

action = function(host, port)
    local socket = nmap.new_socket()
    local status, err = socket:connect(host, port)

    if not status then
        return "Connection failed: " .. err
    end

    local output = {}

    -- Try unit IDs 1-10
    for unit_id = 1, 10 do
        -- Modbus Read Holding Registers (FC 03)
        local trans_id = string.pack(">I2", unit_id)
        local proto_id = "\x00\x00"
        local length = "\x00\x06"
        local func_code = "\x03"
        local start_addr = "\x00\x00"
        local count = "\x00\x0A"

        local request = trans_id .. proto_id .. length .. string.char(unit_id) .. func_code .. start_addr .. count

        status, err = socket:send(request)
        if not status then break end

        status, response = socket:receive()
        if status and #response > 9 then
            local resp_func = string.byte(response, 8)
            if resp_func == 0x03 then
                table.insert(output, string.format("Unit ID %d: ACTIVE", unit_id))
            end
        end
    end

    socket:close()

    if #output > 0 then
        return stdnse.format_output(true, output)
    else
        return "No Modbus slaves responded"
    end
end
