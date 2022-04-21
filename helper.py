import xml.etree.ElementTree as ET
from io import BytesIO

# this will return XML Response with address details
def createXmlResponse(Obj):
    root = ET.Element("root")
    document = ET.ElementTree(root)
    f = BytesIO()
    document.write(f, encoding='utf-8', xml_declaration=True)
    address = ET.Element("address")
    address.text = Obj["address"]
    location = ET.Element("coordinates")
    lat = ET.SubElement(location, "lat")
    lng = ET.SubElement(location, "lng")
    lat.text = Obj["lat"]
    lng.text = Obj["lng"]
    root.append(address)
    root.append(location)
    return root

# this method will extract required address details from XML tree and returns Dictionary of with values
def createXMLResObj(tree):
    xmlValObj = {}
    root = tree.getroot()
    adr = root.findall(".//formatted_address")
    la = root.findall(".//geometry/location/lat")
    ln = root.findall(".//geometry/location/lng")
    for val in adr:
        xmlValObj["address"] = val.text
    for val in la:
        xmlValObj["lat"] = val.text
    for val in ln:
        xmlValObj['lng'] = val.text
    return xmlValObj
