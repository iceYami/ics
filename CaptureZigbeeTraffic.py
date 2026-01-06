# Using Killerbee framework (Zigbee analysis)
sudo apt install python3-usb python3-crypto
git clone https://github.com/riverloopsec/killerbee
cd killerbee
sudo python3 setup.py install

# Capture Zigbee packets (requires compatible adapter: RZUSBSTICK, ApiMote)
zbdump -f zigbee_capture.pcap -c 11  # Channel 11 (2405 MHz)

# Replay captured packets
zbreplay -f zigbee_capture.pcap

# Decrypt (if you have network key)
zbdecrypt -f zigbee_capture.pcap -k 5a:69:67:42:65:65:41:6c:6c:69:61:6e:63:65:30:39
