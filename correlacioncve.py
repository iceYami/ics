#!/usr/bin/env python3
# cve_correlator.py

import json
import requests

def get_cves_for_product(vendor, product, version):
    """
    Query CVE database for vulnerabilities
    """
    # Use NVD API
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "keywordSearch": f"{vendor} {product} {version}"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("result", {}).get("CVE_Items", [])
    return []

# Load asset inventory
with open("asset_inventory.json") as f:
    inventory = json.load(f)

# Check each device for CVEs
for device in inventory["devices"]:
    vendor = device["vendor"]
    model = device["model"]
    firmware = device.get("firmware", "Unknown")

    print(f"\n[*] Checking {device['ip']} - {vendor} {model}")

    cves = get_cves_for_product(vendor, model, firmware)

    if cves:
        print(f"[!] Found {len(cves)} potential CVEs:")
        for cve in cves[:5]:  # Top 5
            cve_id = cve["cve"]["CVE_data_meta"]["ID"]
            description = cve["cve"]["description"]["description_data"][0]["value"]
            print(f"    {cve_id}: {description[:100]}...")

        device["vulnerabilities"] = [cve["cve"]["CVE_data_meta"]["ID"] for cve in cves]
    else:
        print("[+] No known CVEs found")

# Save updated inventory
with open("asset_inventory_with_cves.json", "w") as f:
    json.dump(inventory, f, indent=2)
