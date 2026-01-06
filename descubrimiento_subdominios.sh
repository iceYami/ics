# Using subfinder
subfinder -d company.com -o subdomains.txt

# Using amass (passive mode)
amass enum -passive -d company.com -o amass_subdomains.txt

# Certificate Transparency logs (crt.sh)
curl -s "https://crt.sh/?q=%company.com&output=json" | jq -r '.[].name_value' | sort -u > crt_subdomains.txt

# Combine and deduplicate
cat subdomains.txt amass_subdomains.txt crt_subdomains.txt | sort -u > all_subdomains.txt
