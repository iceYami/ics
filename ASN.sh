# Using whois
whois -h whois.radb.net "Company Name" | grep origin

# Example output:
# origin: AS12345

# Get IP ranges for ASN
whois -h whois.radb.net AS12345 | grep route

# Output:
# route: 203.0.113.0/24
# route: 198.51.100.0/22
