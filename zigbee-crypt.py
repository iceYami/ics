# Extract key from PCAP
git clone https://github.com/edhoedt/zigbee-crypt
python zigbee-crypt.py -f capture.pcap

# If key found, decrypt traffic
wireshark capture.pcap
# Edit → Preferences → Protocols → ZigBee
# Add decryption key
