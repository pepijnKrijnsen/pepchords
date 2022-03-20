from os import (path, system)

def buildSonglist():
    keys = ["id", "artist", "title", "url"]
    values = _getSongValues()
    songlist = [ dict(zip(keys, line.split(","))) for line in values ]
    songlist = _filterScaryChars(songlist)
    songlist.sort(key = lambda v: v["url"])
    return songlist

def _getSongValues():
    with open("songlist.csv") as songs:
        values = songs.read().split("\n")
    return values

def _filterScaryChars(list):
    for v in list:
        v["url"] = v["url"].replace("'", "")
        v["url"] = v["url"].replace("á", "a")
        v["url"] = v["url"].replace("é", "e")
        v["url"] = v["url"].replace("ï", "i")
        v["url"] = v["url"].replace("&-", "")
    return list

def findSong(uid):
    song_path = "songs/" + uid
    if path.isfile(song_path):
        songObject = _readSong(song_path)
    else:
        songObject = song_path
    return songObject

def _readSong(path):
    with open(path) as f:
        return f.read()

def createNewSong(song_object):
    with open(song_object, "w") as f:
        f.write("Title\n\nArtist\n\nKey: ")
    system("$EDITOR " + songObject + " &")
    return

def getSongData(url):
    pass
