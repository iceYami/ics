nmap -Pn -sU -p 47808 --script bacnet-info.nse 192.168.1.0/24

# BACnet uses broadcast Who-Is messages
# More effective with specialized tools like bacnet-stack
