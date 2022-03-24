from os import (path, system, listdir)

def buildSonglist():
    songlist = []
    for song_file in listdir("songs"):
        if path.isfile(path.join("songs", song_file)):
            songlist.append(_getSongData(song_file))
    songlist = _filterScaryChars(songlist)
    songlist.sort(key = lambda v: v["uid"])
    return songlist

def _getSongData(name):
    song_data = dict()
    path = "songs/" + name
    with open(path) as song_file:
        song = song_file.readlines()
    song_data["title"] = song[0]
    song_data["artist"] = song[2]
    song_data["uid"] = name
    return song_data

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
