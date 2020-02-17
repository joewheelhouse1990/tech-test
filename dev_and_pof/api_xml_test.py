import xml.etree.ElementTree as ET
import requests
import time
import xmltodict
import json
from numpy import concatenate

art_resp = requests.get('http://musicbrainz.org/ws/2/artist/?query=artist:Coldplay')
record_url = 'http://musicbrainz.org/ws/2/recording?'

tree = ET.ElementTree(ET.fromstring(art_resp.content))

root = tree.getroot()

artist_list = root[0]

print(f"artist_list[0] attrib: {artist_list[0].attrib} and text {artist_list[0].tag}")
print(f"artist_list[0] attrib: {artist_list[1].attrib} and text {artist_list[1].tag}")

print(f"{artist_list.attrib} and {artist_list.tag}")

artist_count = artist_list.attrib

print(artist_count)
print(artist_count["count"])

for artist in artist_list:
    print(f"artist attrib {artist.attrib} and tag {artist.tag}")
    print(artist[0].text)
    if artist[0].text == "Coldplay":
        _id = artist.attrib["id"]
        print(f"_id has been set to {_id}")

_offset = 0

build_url = f"{record_url}artist={_id}&limit=100&offset={_offset}"

print(build_url)


def fetch_recording_count(xml_tree_obj: ET.ElementTree):

    rcd_root = xml_tree_obj.getroot()

    # get recording list
    record_list = rcd_root[0]

    record_cnt = record_list.attrib["count"]

    return record_cnt


fetch_recs = requests.get(build_url)
recs_tree = ET.ElementTree(ET.fromstring(fetch_recs.content))
get_count = fetch_recording_count(recs_tree)


def fetch_recording_list(record_url, record_count, artist):

    _url = f"{record_url}artist={artist}&limit=100"

    _recordings = []
    _offset = 0
    print(record_count)
    while _offset < int(record_count):
        _build_url = f"{_url}&offset={_offset}"
        fetch_rec = requests.get(_build_url)
        print(f"status code is {fetch_rec.status_code} for url {_build_url}")
        fetch_rec_tree = ET.ElementTree(ET.fromstring(fetch_rec.content))
        _arr_recordings = add_recs_to_array(fetch_rec_tree)
        _recordings = concatenate((_recordings, _arr_recordings), axis=None)
        print(len(_recordings))
        time.sleep(1)
        _offset += 100


def add_recs_to_array(rtree: ET.ElementTree):
    arr = []
    rroot = rtree.getroot()
    rec_tree = rroot[0]
    for rec in rec_tree:
        if rec[0].text not in arr:
        #print(f"rec is {rec[0].text}")
            arr.append(rec[0].text)

    return arr


fetch_recording_list(record_url, get_count, _id)

# for node in root:
#     print(f"node: {node}, attrib: {node.attrib}, tag: {node.tag}")
#     for nnode in node:
#         print(f"nnode: {nnode}, attrib: {nnode.attrib}, tag: {nnode.tag}")
#         if nnode[0].text == 'Coldplay':
#             _id = nnode.attrib['id']
#             print(f"_id set to: {_id}")
#             break
#             print(nnode[0].text)
#             print(nnode[1])

# for child in root:
#     print(child.tag)
#     print(child.attrib)
#     for cchild in child:
#         print(f"the cchild tag {cchild.tag}")
#         print(f"the cchild attrib {cchild.attrib}")
#         print(cchild.find('name'))
#
# print("***")
#
# for name in root.iter('name'):
#     print(name.attrib)
#
# print("***")
#
# for r in root.findall('artist-list'):
#     print(r.find('name'))
#
# o = xmltodict.parse(art_resp.content)
# _json = json.dumps(o, indent=4, sort_keys=True)
#
# print(_json['metadata'])