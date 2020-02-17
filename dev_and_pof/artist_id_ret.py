import musicbrainzngs as mbz
import requests
import asyncio
from dev_and_pof import asyncio_test as asyt


def return_id_from_artist(artist):

    art_ret = mbz.search_artists(artist)
    art_list = art_ret['artist-list']

    for a in art_list:
        if a['name'] == artist and a['ext:score'] == '100':
            _id = a['id']

    return _id


def return_songs_from_artist(artist):

    # set user agent for the app
    mbz.set_useragent('tech-test (contact-joe.wheelhouse@gmail.com', '0')
    arid = return_id_from_artist(artist)

    if arid is None:
        print("No artist id found")
        return None
    else:
        rec_ret = mbz.browse_recordings(arid, limit=100)
        return rec_ret


def get_lyrics_from_songs(artist, songs):

    proxies = { "http": None, "https": None}

    for s in songs:
        build_url = f"https://api.lyrics.ovh/v1/{artist}/{s}/"
        fetch_resp = requests.get(build_url, proxies=proxies)
        print(fetch_resp.status_code)
        print(fetch_resp.json())


def create_unique_song_list(songs):

    arr = []
    for s in songs:
        if s['title'] not in arr:
            arr.append(s['title'])

    print(arr)
    return arr


def create_urls(songs, artist):

    urls = []
    for song in songs:
        url = f"https://api.lyrics.ovh/v1/{artist}/{song}"
        urls.append(url)

    return urls


if __name__ == '__main__':

    _logger = asyt.setup_log()

    _artist = 'Lewis Capaldi'
    _ret = return_songs_from_artist(_artist)
    _songs = _ret['recording-list']

    song_list = create_unique_song_list(_songs)
    url_list = create_urls(song_list, _artist)
    asyncio.run(asyt.work_through_urls(url_list, _logger))
    # get_lyrics_from_songs(_artist, song_list)


