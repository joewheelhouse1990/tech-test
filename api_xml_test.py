import xml.etree.ElementTree as ET
import requests
import xmltodict
import json

art_resp = requests.get('http://musicbrainz.org/ws/2/artist/?query=artist:Coldplay')

print(art_resp.content)

tree = ET.ElementTree(ET.fromstring(art_resp.content))

print(tree)

root = tree.getroot()

print(root.tag)
print(root.attrib)

for child in root:
    print(child.tag)
    print(child.attrib)
    for cchild in child:
        print(f"the cchild tag {cchild.tag}")
        print(f"the cchild attrib {cchild.attrib}")
        print(cchild.find('name'))

print("***")

for name in root.iter('name'):
    print(name.attrib)

print("***")

for r in root.findall('artist-list'):
    print(r.find('name'))

o = xmltodict.parse(art_resp.content)
_json = json.dumps(o, indent=4, sort_keys=True)

print(_json['metadata'])