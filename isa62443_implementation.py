# isa62443_implementation.py
# Implement ISA/IEC 62443 zone and conduit model

import ipaddress
from enum import Enum

class SecurityLevel(Enum):
    SL0 = 0
    SL1 = 1
    SL2 = 2
    SL3 = 3
    SL4 = 4

class SecurityZone:
    def __init__(self, name, security_level, network, criticality):
        self.name = name
        self.security_level = security_level
        self.network = ipaddress.ip_network(network)
        self.criticality = criticality  # safety, production, business
        self.assets = []

    def add_asset(self, asset):
        """Add asset to zone"""
        if ipaddress.ip_address(asset['ip']) in self.network:
            self.assets.append(asset)
            return True
        return False

    def get_security_requirements(self):
        """Return security controls required for this SL"""
        requirements = {
            SecurityLevel.SL0: [],
            SecurityLevel.SL1: [
                'User authentication',
                'Audit logging'
            ],
            SecurityLevel.SL2: [
                'Multi-factor authentication',
                'Encryption in transit',
                'Intrusion detection',
                'Security event logging'
            ],
            SecurityLevel.SL3: [
                'Role-based access control',
                'Strong encryption (AES-256)',
                'Network segmentation',
                'Continuous monitoring',
                'Integrity verification'
            ],
            SecurityLevel.SL4: [
                'Defense-in-depth',
                'Unidirectional gateways',
                'Hardware security modules',
                'Tamper detection',
                'Air-gapped networks',
                'Real-time threat intelligence'
            ]
        }

        # Cumulative requirements
        req_list = []
        for level in SecurityLevel:
            req_list.extend(requirements[level])
            if level == self.security_level:
                break

        return list(set(req_list))  # Remove duplicates

class Conduit:
    def __init__(self, name, source_zone, dest_zone):
        self.name = name
        self.source_zone = source_zone
        self.dest_zone = dest_zone
        self.allowed_protocols = []
        self.enforcement_mechanism = None
        self.direction = 'bidirectional'  # or 'unidirectional'

    def determine_required_sl(self):
        """Conduit SL = max(source SL, destination SL)"""
        return max(self.source_zone.security_level,
                  self.dest_zone.security_level)

    def add_protocol(self, protocol, port, direction='bidirectional'):
        """Add allowed protocol to conduit"""
        self.allowed_protocols.append({
            'protocol': protocol,
            'port': port,
            'direction': direction
        })

    def get_enforcement_requirements(self):
        """Determine required enforcement mechanism based on SL"""
        required_sl = self.determine_required_sl()

        if required_sl == SecurityLevel.SL4:
            return 'Unidirectional gateway with DPI and encrypted tunnels'
        elif required_sl == SecurityLevel.SL3:
            return 'Industrial firewall with DPI and IDS'
        elif required_sl == SecurityLevel.SL2:
            return 'Firewall with protocol filtering'
        else:
            return 'Basic ACLs'

# Example: Power plant implementation
def design_power_plant_network():
    # Define zones
    turbine_control = SecurityZone(
        name='Turbine Control System',
        security_level=SecurityLevel.SL4,  # Safety-critical
        network='10.10.10.0/24',
        criticality='safety'
    )

    scada_operations = SecurityZone(
        name='SCADA Operations',
        security_level=SecurityLevel.SL3,
        network='10.10.20.0/24',
        criticality='production'
    )

    historian_dmz = SecurityZone(
        name='Historian DMZ',
        security_level=SecurityLevel.SL2,
        network='10.10.30.0/24',
        criticality='business'
    )

    # Add assets
    turbine_control.add_asset({'ip': '10.10.10.10', 'type': 'Safety PLC', 'vendor': 'Siemens'})
    scada_operations.add_asset({'ip': '10.10.20.50', 'type': 'SCADA Server', 'vendor': 'Ignition'})

    # Define conduits
    scada_to_turbine = Conduit(
        name='SCADA to Turbine Control',
        source_zone=scada_operations,
        dest_zone=turbine_control
    )
    scada_to_turbine.add_protocol('Modbus TCP', 502)
    scada_to_turbine.add_protocol('OPC UA', 4840)

    turbine_to_historian = Conduit(
        name='Turbine to Historian',
        source_zone=turbine_control,
        dest_zone=historian_dmz
    )
    turbine_to_historian.direction = 'unidirectional'  # One-way only
    turbine_to_historian.add_protocol('OPC UA', 4840, direction='outbound')

    # Generate security requirements
    print(f"Zone: {turbine_control.name}")
    print(f"Security Level: {turbine_control.security_level.name}")
    print(f"Required Controls:")
    for control in turbine_control.get_security_requirements():
        print(f"  - {control}")

    print(f"\nConduit: {scada_to_turbine.name}")
    print(f"Required SL: SL-{scada_to_turbine.determine_required_sl().value}")
    print(f"Enforcement: {scada_to_turbine.get_enforcement_requirements()}")

design_power_plant_network()
