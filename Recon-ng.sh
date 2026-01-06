# Install
sudo apt install recon-ng

# Launch
recon-ng

# Load modules
marketplace install all

# Create workspace
workspaces create company_osint

# Add domain
db insert domains domain company.com

# Run modules
modules load recon/domains-hosts/bing_domain_web
run

modules load recon/hosts-hosts/resolve
run

# Export results
show hosts
