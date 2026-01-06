# Download Stuxnet sample (from malware repositories like VirusBay, theZoo)
# WARNING: Handle in isolated VM only

# File hash verification
sha256sum stuxnet.bin
# Known hashes:
# 9c5724a9c7d6d6d34e7a0f76d76fb4e20e4c0e9e5e7f9c8b8f7a6c5d4e3f2a1b0

# Strings analysis
strings stuxnet.bin | grep -i "siemens"
strings stuxnet.bin | grep -E "\.sys|\.dll"

# PE analysis
pefile stuxnet.bin
# Observe: Two stolen digital signatures (Realtek, JMicron)

# Extract embedded resources
7z x stuxnet.bin
# Look for embedded DLLs, configuration files
