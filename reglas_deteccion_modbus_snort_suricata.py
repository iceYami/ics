# Detect Modbus write operations
alert tcp any any -> any 502 (msg:"MODBUS Write Single Register"; content:"|06|"; offset:7; depth:1; sid:1000001;)
alert tcp any any -> any 502 (msg:"MODBUS Write Multiple Registers"; content:"|10|"; offset:7; depth:1; sid:1000002;)

# Detect Modbus from unexpected source
alert tcp !$MODBUS_MASTERS any -> any 502 (msg:"MODBUS from unauthorized source"; sid:1000003;)

# Detect Modbus diagnostic functions
alert tcp any any -> any 502 (msg:"MODBUS Diagnostic Function"; content:"|08|"; offset:7; depth:1; sid:1000004;)
