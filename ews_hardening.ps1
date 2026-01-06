# ews_hardening.ps1 - Harden EWS against supply chain attacks

# Enable AppLocker (application whitelisting)
New-AppLockerPolicy -RuleType Publisher -Path "C:\Program Files\Siemens\*" -Action Allow
New-AppLockerPolicy -RuleType Publisher -Path "C:\Program Files (x86)\Rockwell Software\*" -Action Allow
New-AppLockerPolicy -RuleType Hash -Path * -Action Deny

# Disable unnecessary services
$services = @("RemoteRegistry", "WinRM", "TeamViewer")
foreach ($svc in $services) {
    Stop-Service $svc
    Set-Service $svc -StartupType Disabled
}

# Enable advanced logging
auditpol /set /subcategory:"Process Creation" /success:enable
auditpol /set /subcategory:"DLL Loading" /success:enable

# USB device control (only allow approved devices)
# Group Policy: Computer Configuration > Administrative Templates > System > Device Installation > Device Installation Restrictions
