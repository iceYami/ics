# Detect DNP3 Direct Operate without SELECT
alert tcp any any -> any 20000 (
    msg:"DNP3 DIRECT OPERATE - Bypasses Safety";
    content:"|05 64|"; depth:2;
    content:"|05|"; distance:8; within:1;  # Function 5
    classtype:attempted-admin;
    sid:3000001;
)

# Detect IEC 104 mass breaker trips
alert tcp any any -> any 2404 (
    msg:"IEC 104 Multiple Breaker Trips";
    content:"|68|"; depth:1;
    content:"|2D 01|"; distance:4; within:2;  # Type 45, VSQ=1
    threshold:type threshold, track by_src, count 10, seconds 60;
    classtype:attempted-dos;
    sid:3000002;
)

# Detect GOOSE spoofing (Ethernet-level)
alert any any -> any any (
    msg:"IEC 61850 GOOSE Message Detected";
    content:"|88 B8|"; depth:2; offset:12;  # GOOSE Ethertype
    classtype:policy-violation;
    sid:3000003;
)

# Detect IEC 104 interrogation (reconnaissance)
alert tcp any any -> any 2404 (
    msg:"IEC 104 Interrogation Command";
    content:"|68|"; depth:1;
    content:"|64|"; distance:5; within:1;  # Type 100
    classtype:attempted-recon;
    sid:3000004;
)
