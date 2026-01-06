# Using amass
amass intel -asn 12345 -whois

# Using bgpview API
curl -s "https://api.bgpview.io/asn/12345/prefixes" | jq -r '.data.ipv4_prefixes[].prefix'

# Save IP ranges
curl -s "https://api.bgpview.io/asn/12345/prefixes" | jq -r '.data.ipv4_prefixes[].prefix' > target_ranges.txt
