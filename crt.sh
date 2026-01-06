# Search for OPC UA certificates
curl "https://crt.sh/?q=%opcua%&output=json" | jq .

# Search by organization
curl "https://crt.sh/?q=%Electric%Company%&output=json" | jq .

# Identify subdomains
curl "https://crt.sh/?q=%.company.com&output=json" | jq '.[].name_value' | sort -u
