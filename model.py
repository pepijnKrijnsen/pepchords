from os import (path, system, listdir)

def buildSonglist():
    songlist = []
    for song_file in listdir("songs"):
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

def getSong(uid):
    with open("songs/" + uid) as songfile:
        song_raw = songfile.read()
    items = song_raw.split("\n\n")
    song = dict(uid = uid)
    song["title"] = items.pop(0)
    song["artist"] = items.pop(0)
    song["metadata"] = dict()
    for line in items.pop(0).split("\n"):
        pair = line.split(": ")
        song["metadata"][pair[0]] = pair[1]
    song["music_lyrics_list"] = items
    song["music_lyrics_string"] = ""
    for el in items:
        song["music_lyrics_string"] += el + "\n\n"
    song["music_lyrics_string"] = song["music_lyrics_string"][:-3]
    return song

def createNewSong(song_object):
    with open(song_object, "w") as f:
        f.write("Title\n\nArtist\n\nKey: ")
    system("$EDITOR " + songObject + " &")
    return

def backUpSong(uid):
    system("mv songs/" + uid + " song_backups/" + uid)
    return

def createSongData(dict):
    song_data = dict["title"] + "\n\n"
    song_data += dict["artist"] + "\n\n"
    song_data += "Key: " + dict["Key"] + "\n"
    song_data += "Capo: " + dict["Capo"] + "\n\n"
    song_data += dict["music_lyrics"]
    print(dict["music_lyrics"])
    return song_data
