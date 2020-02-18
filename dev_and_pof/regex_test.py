import re


def find_remixes_and_live(song, arr):

    res = re.sub(r'\ ?\((.*?)\)', '', song)
    print(f"song after brackets removed removed: {res}")
    if res not in arr:
        print("res is in arr")
        return True
    else:
        return False


def loop_songs():

    arr = []
    songs = ["Yellow", "Yellow (live in chicago)", "trouble", "trouble (remix radio dj)"]
    for s in songs:
        print(f"s is {s}")
        if find_remixes_and_live(s, arr):
            arr.append(s)
        print(arr)


loop_songs()