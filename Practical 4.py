"""
CYB 304 - Week 2 | Practical 4: Working with XML Files
=======================================================
Objective: Parse XML data using Python's built-in `xml.etree.ElementTree`
module.  XML (Extensible Markup Language) is widely used in enterprise
systems, banking SWIFT messages, healthcare records (HL7/FHIR), and
legacy security appliance log formats.

Real-world use-case:
  Banking SWIFT wire-transfer messages use XML.
  Enterprise security appliances (firewalls, IDS) export event logs as XML.
  SAML authentication tokens — used in SSO — are XML-based.
"""

import xml.etree.ElementTree as ET


# ------------------------------------------------------------------ #
#  STEP 1 — Parse a simple XML string                                 #
# ------------------------------------------------------------------ #

SIMPLE_XML = """<student>
    <name>Ada</name>
    <department>Cybersecurity</department>
    <level>300</level>
</student>"""


def parse_simple_xml():
    """
    ET.fromstring() parses an XML string and returns the root Element.
    root.find('tag') searches for the FIRST child with that tag name.
    .text returns the text content between the opening and closing tags.
    """
    print("=" * 55)
    print("PRACTICAL 4 — XML File Handling")
    print("=" * 55)

    print("\n[Step 1] Raw XML string:")
    print(SIMPLE_XML)

    root = ET.fromstring(SIMPLE_XML)

    print("\n  Parsed values:")
    print(f"    Name       : {root.find('name').text}")        # Ada
    print(f"    Department : {root.find('department').text}")  # Cybersecurity
    print(f"    Level      : {root.find('level').text}")       # 300


# ------------------------------------------------------------------ #
#  STEP 2 — Parse XML with multiple records (a list/collection)       #
# ------------------------------------------------------------------ #

STUDENTS_XML = """<students>
    <student id="001">
        <name>John</name>
        <score>78</score>
        <department>Cybersecurity</department>
    </student>
    <student id="002">
        <name>Mary</name>
        <score>85</score>
        <department>Computer Science</department>
    </student>
    <student id="003">
        <name>Ahmed</name>
        <score>92</score>
        <department>Cybersecurity</department>
    </student>
</students>"""


def parse_xml_collection():
    """
    root.findall('tag') returns a LIST of all matching child elements.
    element.get('attr') reads an XML attribute (e.g. id="001").
    """
    print("\n[Step 2] XML collection — multiple student records:")

    root = ET.fromstring(STUDENTS_XML)

    # Iterate over every <student> element
    print(f"\n  {'ID':<6} {'Name':<10} {'Score':<8} {'Department'}")
    print(f"  {'-'*6} {'-'*10} {'-'*8} {'-'*20}")

    for student in root.findall("student"):
        sid   = student.get("id")
        name  = student.find("name").text
        score = student.find("score").text
        dept  = student.find("department").text
        print(f"  {sid:<6} {name:<10} {score:<8} {dept}")


# ------------------------------------------------------------------ #
#  STEP 3 — Parse a realistic security event log in XML               #
# ------------------------------------------------------------------ #

SECURITY_LOG_XML = """<security_events>
    <event id="E001" severity="HIGH">
        <timestamp>2025-05-23T08:30:00Z</timestamp>
        <type>Brute Force Attack</type>
        <source_ip>203.0.113.45</source_ip>
        <target>admin portal</target>
        <attempts>47</attempts>
        <blocked>true</blocked>
    </event>
    <event id="E002" severity="MEDIUM">
        <timestamp>2025-05-23T09:01:00Z</timestamp>
        <type>Port Scan</type>
        <source_ip>198.51.100.22</source_ip>
        <target>internal network</target>
        <attempts>1</attempts>
        <blocked>false</blocked>
    </event>
</security_events>"""


def parse_security_xml_log():
    """
    Real firewalls and IDS systems export alerts as XML.
    We extract and display actionable fields for an analyst.
    """
    print("\n[Step 3] Security Event Log (XML → analyst view):")

    root = ET.fromstring(SECURITY_LOG_XML)

    for event in root.findall("event"):
        eid      = event.get("id")
        severity = event.get("severity")
        etype    = event.find("type").text
        src_ip   = event.find("source_ip").text
        attempts = event.find("attempts").text
        blocked  = event.find("blocked").text

        print(f"\n  Event  : {eid}")
        print(f"  Severity: {severity}")
        print(f"  Type    : {etype}")
        print(f"  Src IP  : {src_ip}")
        print(f"  Attempts: {attempts}")
        print(f"  Blocked : {blocked}")


# ------------------------------------------------------------------ #
#  STEP 4 — Write XML to a file and read it back                      #
# ------------------------------------------------------------------ #

def write_and_read_xml_file():
    """
    ET.ElementTree(root).write() serialises the element tree to a file.
    ET.parse() reads it back.
    """
    # Build an XML tree programmatically
    root = ET.Element("students")

    for name, score in [("John", 78), ("Mary", 85)]:
        student = ET.SubElement(root, "student")
        ET.SubElement(student, "name").text  = name
        ET.SubElement(student, "score").text = str(score)

    tree = ET.ElementTree(root)
    tree.write("students.xml", encoding="unicode", xml_declaration=True)
    print("\n[Step 4] Written students.xml")

    # Read back
    parsed_tree = ET.parse("students.xml")
    parsed_root = parsed_tree.getroot()
    print("  Read back:")
    for s in parsed_root.findall("student"):
        print(f"    {s.find('name').text} — Score: {s.find('score').text}")

    import os
    os.remove("students.xml")


# ------------------------------------------------------------------ #
#  MAIN                                                               #
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    parse_simple_xml()
    parse_xml_collection()
    parse_security_xml_log()
    write_and_read_xml_file()
    print("\n[Done] XML practical complete.")
