# typosquatting_campaign.py - Register similar domains
legitimate_domains = [
    "siemens.com",
    "rockwellautomation.com",
    "schneider-electric.com",
    "aveva.com"
]

typosquat_domains = [
    "siem3ns.com",  # 'e' -> '3'
    "rockwellautomation.net",  # .com -> .net
    "schneider-elec.com",  # shortened
    "aveva-software.com"  # added keyword
]

# Host malicious software downloads
# SEO optimization to rank in Google for "download TIA Portal"
# Serve trojanized installers to unsuspecting engineers
