from os import (path, system)

def buildSonglist():
    keys = ["id", "artist", "title", "uid"]
    values = _getSongValues()
    songlist = [ dict(zip(keys, line.split(","))) for line in values ]
    songlist = _filterScaryChars(songlist)
    songlist.sort(key = lambda v: v["uid"])
    return songlist

def _getSongValues():
    with open("songlist.csv") as songs:
        values = songs.read().split("\n")
    return values

def _filterScaryChars(songlist):
    for el in songlist:
        el["uid"] = el["uid"].replace("'", "")
        el["uid"] = el["uid"].replace("á", "a")
        el["uid"] = el["uid"].replace("é", "e")
        el["uid"] = el["uid"].replace("ï", "i")
        el["uid"] = el["uid"].replace("&-", "")
    return songlist

def findSong(uid):
    song_path = "songs/" + uid
    if not path.isfile(song_path):
        return False
    else:
        return _readSong(song_path)

def _readSong(path):
    with open(path) as f:
        return f.read()

def parseSong(songObject):
    items = songObject.split("\n\n")
    song = dict()
    keys = ["title", "artist", "metadata"]
    for k in keys:
        song[k] = items.pop(0)
    print(items)
    song["metadata"] = song["metadata"].split("\n")
    song["chords_lyrics"] = items
    return song

def createNewSong(song_object):
    with open(song_object, "w") as f:
        f.write("Title\n\nArtist\n\nKey: ")
    system("$EDITOR " + songObject + " &")
    return

def getSongData(url):
    pass
