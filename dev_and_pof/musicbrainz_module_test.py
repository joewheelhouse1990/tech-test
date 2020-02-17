import musicbrainzngs as mbz
import json

mbz.set_useragent('tech-test (contact-joe.wheelhouse@gmail.com', '0')

_ret = mbz.search_artists('Coldplay')
_lcr = mbz.search_artists('Queen')
_cap = mbz.search_artists('Lewis Capaldi')

print(_ret)

i = 0
for l in _cap['artist-list']:
    if i < 10:
        if l['ext:score'] == '100':
            print(l['id'])
            _id = l['id']
        print(l)
    else:
        break
    i += 1

recs = mbz.get_artist_by_id(_id, includes='recordings')

_json = json.dumps(recs, indent=4)

print(_json)

test_id = "cc197bad-dc9c-440d-a5b5-d52ba2e14234"
count = "2731"

_offset = 0
while int(_offset) < int(count):
    _ret = mbz.browse_recordings(test_id, limit=100, offset=_offset)
    arr = []
    print(_ret)
    _artist_json = _ret["recording-list"]
    for r in _artist_json:
        print(r)
        if r["title"] not in arr:
            arr.append(r["title"])
    print(len(arr))
    print(arr)
    _offset += 100

