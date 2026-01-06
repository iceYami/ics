nmap -Pn -sT -p 102,502,1089,1091,2222,4840,20000,44818,47808 \
     --max-retries 1 --max-rtt-timeout 500ms --scan-delay 100ms \
     --min-rate 10 --max-rate 50 \
     192.168.1.0/24 -oA ics_scan_conservative
