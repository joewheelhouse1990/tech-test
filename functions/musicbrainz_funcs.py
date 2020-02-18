import xml.etree.ElementTree as ET
import requests
import time
import musicbrainzngs as mb
import re
from numpy import concatenate
import asyncio
from aiohttp import ClientSession


# global variables #
# url for musicbrainz api
_MBRAINZ = "http://musicbrainz.org/ws/2/"
# indices position for getting artist from element tree
_IGET_ARTIST = 0
# indices position for getting artist name from element tree
_IGET_NAME = 0
# indices position for getting the recordings count from element tree
_IGET_RCRD = 0
# indices position for getting the recordings from artist recordings element tree
_IGET_RECS = 0
# indices position for the recording title
_IGET_REC_NAME = 0
# indices name for getting the artist id from an artist
_SGET_ID = "id"
# limit for returning the artist id count
_LIMIT_LOW = 1
# limit for returning recordings
_LIMIT = 100
# offset starting point
_OFFSET = 0
# amount of time to sleep function
_SLEEP = 0.5


def fetch_artist_id(artist):
    """
    gets the artist id for a given artist name from the musicbrainz api
    :param artist: artist name as string
    :return: musicbrainz artist id
    """
    build_url = f"{_MBRAINZ}artist/?query=artist:{artist}"

    response = requests.get(build_url)
    artist_tree = ET.ElementTree(ET.fromstring(response.content))
    artist_root = artist_tree.getroot()[_IGET_ARTIST]

    for a in artist_root:
        if a[_IGET_NAME].text == artist:
            _id = a.attrib[_SGET_ID]
            # leave loop and return id
            return _id


def fetch_recording_count(artist_id):
    """
    given an artist id fetch the number of recordings
    :param artist_id: musicbrainz id to get artist recordings
    :return: count of recordings for loop
    """
    build_url = f"{_MBRAINZ}recording?artist={artist_id}&limit={_LIMIT_LOW}&offset={_OFFSET}"

    try:
        response = requests.get(build_url)
        rcrd_tree = ET.ElementTree(ET.fromstring(response.content))
        rcrd_root = rcrd_tree.getroot()[_IGET_RCRD]

        rcrd_count = rcrd_root.attrib["count"]

        return rcrd_count
    except KeyError as e:
        print("Write to log/console: No artist with that id")
        raise e


def fetch_recording_list_module(artist_id, record_count):

    mb.set_useragent('tech-test (contact-joe.wheelhouse@gmail.com', '0')
    _offset = _OFFSET
    _recordings = []
    while _offset < int(record_count):
        _ret = mb.browse_recordings(artist_id, limit=_LIMIT, offset=_offset)
        _rec_json = _ret["recording-list"]
        for r in _rec_json:
            s = r["title"].upper()
            if (
                    check_brackets_in_arr(s, _recordings) and
                    check_cases_in_arr(s, _recordings)
            ):
                _recordings.append(s)
        _offset += 100
    return _recordings


def check_brackets_in_arr(song, arr):

    res = re.sub(r'\ ?\((.*?)\)', '', song)
    if res not in arr:
        return True


def check_cases_in_arr(song, arr):

    if song not in arr:
        return True


def check_interlude_in_arr(song, arr):

    res = re.sub(r'\ ?\[(.*?)\]|\ ?\((.*?)\)', '', song)
    if not(res == ''):
        return True


# functions that deal with xml fetch - alternative to python musicbrainz module


def add_recs_to_array_from_tree(rtree: ET.ElementTree):
    """
    given an xml tree return the unique recordings as an array
    :param rtree: xml element tree containing recordings
    :return: array unique records for tree
    """
    # not case sensitive - remove any replicas.
    arr = []
    root = rtree.getroot()
    rec_tree = root[_IGET_RECS]
    for rec in rec_tree:
        print(f"checking if this is in the array: {rec[_IGET_REC_NAME].text.upper()}")
        if rec[_IGET_REC_NAME].text.upper() not in arr:
            arr.append(rec[_IGET_REC_NAME].text.upper())
            print(f"adding to array: {rec[_IGET_REC_NAME].text.upper()}")

    return arr


def fetch_recording_list(artist_id, record_count):
    """
    given an artist_id and record count fetch all the recordings
    :param artist_id: musicbrainz artist id
    :param record_count: number of recordings for an artist
    :return: array of recordings by artist
    """

    _url_base = f"{_MBRAINZ}recording?artist={artist_id}&limit={_LIMIT}"

    # empty array of recordings and set offset to be 0 to start while loop
    _recordings = []
    _offset = _OFFSET

    # while offset is less than record count, the next get will always include the results we need
    while _offset < int(record_count):
        # build url and get request
        _build_url = f"{_url_base}&offset={_offset}"
        fetch_rec = requests.get(_build_url)
        # put into element tree
        fetch_rec_tree = ET.ElementTree(ET.fromstring(fetch_rec.content))
        # fetch array of recordings
        _arr_recordings = add_recs_to_array_from_tree(fetch_rec_tree)
        # concatenate the new results with the existing
        _recordings = concatenate((_recordings, _arr_recordings), axis=None)
        # sleep to not get booted off the api
        time.sleep(_SLEEP)
        # add get limit to the offset to get next page of records
        _offset += _LIMIT

    return _recordings
