# Ping sweep (identify live hosts)
sudo nmap -sn 10.10.10.0/24 -oA ping_sweep

# Extract live IPs
cat ping_sweep.gnmap | grep "Status: Up" | awk '{print $2}' > live_hosts.txt

# Port scan (ICS ports only, slow rate)
sudo nmap -Pn -sT -p 80,102,161,443,502,1089,1091,2222,4840,8080,20000,44818,47808 \
    --max-retries 1 --scan-delay 100ms --max-rate 50 \
    -iL live_hosts.txt -oA ics_port_scan

# Service version detection (minimal)
sudo nmap -Pn -sT -sV --version-intensity 0 \
    -p 102,502,44818 \
    -iL live_hosts.txt -oA ics_service_scan
