# Extract unique IPs communicating on ICS ports
tshark -r capture.pcap -Y "tcp.port == 502 || tcp.port == 102 || tcp.port == 44818 || tcp.port == 20000" \
       -T fields -e ip.src -e ip.dst | sort -u

# Count protocol distribution
tshark -r capture.pcap -q -z io,phs
