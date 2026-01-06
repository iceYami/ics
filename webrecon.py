# Identify web servers
cat ics_port_scan.gnmap | grep "80/open\|443/open\|8080/open"

# Enumerate web interfaces
for ip in $(cat web_servers.txt); do
    echo "[*] Scanning $ip"

    # Identify technology
    whatweb http://$ip

    # Directory enumeration (gentle)
    gobuster dir -u http://$ip -w /usr/share/wordlists/dirb/common.txt -t 5 -q -o ${ip}_dirs.txt

    # Nikto scan (slow mode)
    nikto -h http://$ip -Tuning 1 -o ${ip}_nikto.txt
done

# Document findings:
# - HMI login pages (default credentials?)
# - Exposed configuration interfaces
# - Version disclosure (check for CVEs)
