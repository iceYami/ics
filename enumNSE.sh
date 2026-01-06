# Modbus discovery
sudo nmap -Pn -sT -p 502 --script modbus-discover.nse 10.10.10.10 -oN modbus_enum.txt

# S7comm enumeration
sudo nmap -Pn -sT -p 102 --script s7-info.nse 10.10.10.11 -oN s7_enum.txt

# OPC UA discovery
sudo nmap -Pn -sT -p 4840 --script opcua-info.nse 10.10.10.50 -oN opcua_enum.txt

# Ethernet/IP (if applicable)
sudo nmap -Pn -sU -p 44818 --script enip-info.nse 10.10.10.12 -oN enip_enum.txt

# Document findings:
# - Device models and serial numbers
# - Firmware versions
# - Available function codes/services
# - Vendor-specific information
