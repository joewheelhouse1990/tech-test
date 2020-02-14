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
