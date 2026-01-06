# verify_installer.sh - Verify software installer authenticity
INSTALLER="TIA_Portal_V17_Update.exe"

# 1. Check digital signature
osslsigncode verify -in $INSTALLER

# 2. Verify hash against vendor website
VENDOR_HASH="a1b2c3d4e5f6..."  # From Siemens website
ACTUAL_HASH=$(sha256sum $INSTALLER | awk '{print $1}')

if [ "$VENDOR_HASH" != "$ACTUAL_HASH" ]; then
    echo "[!] ALERT: Hash mismatch - possible trojan!"
    echo "[!] Expected: $VENDOR_HASH"
    echo "[!] Actual:   $ACTUAL_HASH"
    exit 1
fi

# 3. Sandbox execution before deployment
# Run in isolated VM, monitor behavior
