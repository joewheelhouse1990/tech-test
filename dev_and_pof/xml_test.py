# from urllib.request import Request, urlopen
#
#
# response = Request(api_add)
#
# response_body = urlopen(response).read()
#
# print(response_body)

# import requests
#
# api_add = "https://musicbrainz.org/ws/2/artist?query=Coldplay"
# response = requests.get(api_add)
#
# print(response.status_code)

import xml.etree.ElementTree as ET
import json

tree = ET.parse("C:\\Temp\\artist.xml")

root = tree.getroot()

print(f"root.findall{root.findall('.')}")

for node in root:
    print(node.attrib)
    print(node.tag)

print(root[0])

print(root.findall('{http://musicbrainz.org/ns/mmd-2.0#}artist'))

artist_list = root[0]

print(f"xpath cap {artist_list.findall('./artist-list/artist/')}")

print(artist_list.attrib)

for artist in artist_list.iter('artist'):
    print(artist.attrib)

print("loop through")

for node in root:
    print(f"node: {node}, attrib: {node.attrib}, tag: {node.tag}")
    for nnode in node:
        print(f"nnode: {nnode}, attrib: {nnode.attrib}, tag: {nnode.tag}")
        if nnode[0].text == 'Coldplay':
            _id = nnode.attrib['id']
            print(f"_id set to: {_id}")
            break
            print(nnode[0].text)
            print(nnode[1])

with open("C:\\Temp\\learning\\recording.json") as of:
    _json = json.load(of)

print(_json)