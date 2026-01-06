#!/usr/bin/env python3
import requests
import json
import subprocess

def osint_pipeline(target_domain):
    """
    Automated OSINT collection for OT infrastructure
    """
    results = {
        "domain": target_domain,
        "subdomains": [],
        "ips": [],
        "technologies": [],
        "employees": []
    }

    # Step 1: Subdomain enumeration
    print("[*] Enumerating subdomains...")
    cmd = f"subfinder -d {target_domain} -silent"
    subdomains = subprocess.check_output(cmd, shell=True).decode().splitlines()
    results["subdomains"] = subdomains

    # Step 2: Certificate Transparency
    print("[*] Checking certificate transparency logs...")
    crt_url = f"https://crt.sh/?q=%{target_domain}&output=json"
    response = requests.get(crt_url)
    if response.status_code == 200:
        certs = response.json()
        for cert in certs:
            results["subdomains"].append(cert.get("name_value"))

    results["subdomains"] = list(set(results["subdomains"]))

    # Step 3: Shodan search for exposed services
    print("[*] Searching Shodan for exposed ICS services...")
    # (Requires Shodan API key)

    # Step 4: GitHub search
    print("[*] Searching GitHub for leaks...")
    # (Requires GitHub API)

    # Save results
    with open(f"{target_domain}_osint.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"[+] OSINT collection complete. Results saved to {target_domain}_osint.json")
    return results

# Usage
# osint_pipeline("company.com")
