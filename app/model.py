from os import (path, system, listdir)

import persistence

def getSecret():
    secret = persistence.readSecretKeyFile()
    return secret

def buildSonglist():
    songlist = [ _getSongData(song_file) for song_file in listdir("songs") ]
    songlist.sort(key = lambda v: v["uid"])
    return songlist

def _getSongData(uid):
    song_lines = persistence.readSongFile_toLines(uid)
    song_data = dict()
    song_data["title"] = song_lines[0]
    song_data["artist"] = song_lines[2]
    song_data["uid"] = uid
    return song_data

def checkForArtistAndTitle(dict):
    message = ""
    if not dict["title"]:
        message = "Title is required!"
    elif not dict["artist"]:
        message = "Artist is required!"
    return message

def createAndPersistSongString(dict):
    song_uid = _createSongUID(dict["title"], dict["artist"])
    song_data_string = _convertNewSongForm_toString(dict)
    persistence.writeSongFile(song_uid, song_data_string)
    return

def _createSongUID(title, artist):
    safe_artist = _filterScaryChars(artist.lower().replace(" ", "-"))
    safe_title = _filterScaryChars(title.lower().replace(" ", "-"))
    return safe_artist + "-" + safe_title

def _filterScaryChars(string):
    string = string.replace("'", "")
    string = string.replace("á", "a")
    string = string.replace("é", "e")
    string = string.replace("ï", "i")
    string = string.replace("&-", "")
    return string

def _convertNewSongForm_toString(dict):
    song_data = dict["title"] + "\n\n"
    song_data += dict["artist"] + "\n\n"
    song_data += "capo: " + dict["capo"] + "\n"
    song_data += "key: " + dict["key"] + "\n"
    song_data += "tempo: " + dict["tempo"] + "\n\n"
    song_data += "font size: 16" + "\n\n"
    song_data += dict["music_lyrics"]
    return song_data

def getSongObject(uid):
    song_raw = persistence.readSongFile(uid)
    song_object = _convertSongString_toDict(song_raw)
    song_object["uid"] = uid
    return song_object

def _convertSongString_toDict(song_raw):
    items = song_raw.split("\n\n")
    song = dict()
    song["title"] = items.pop(0)
    song["artist"] = items.pop(0)
    song["metadata"] = dict()
    for line in items.pop(0).split("\n"):
        pair = line.split(": ")
        song["metadata"][pair[0]] = pair[1]
    song["fontsize"] = float(items.pop(0).split(": ")[1])
    song["music_lyrics"] = items
    return song

def editSong(uid):
    song_raw = persistence.readSongFile(uid)
    song_object = _convertSongString_toDict(song_raw)
    song_object["uid"] = uid
    song_object["music_lyrics_string"] = _convertList_toString(
            song_object["music_lyrics"])
    return song_object

def _convertList_toString(list):
    string = ""
    for el in list:
        string += el + "\n\n"
    string = string[:-2]
    return string

def updateFontSize(uid, change):
    song_object = _convertSongString_toDict(persistence.readSongFile(uid))
    song_object["fontsize"] = str(song_object["fontsize"] + (change / 2))
    song_string = _convertSongDict_toString(song_object)
    persistence.writeSongFile(uid, song_string)
    return

def _convertSongDict_toString(song_object):
    song_data = song_object["title"] + "\n\n"
    song_data += song_object["artist"] + "\n\n"
    song_data += "capo: " + song_object["metadata"]["capo"] + "\n"
    song_data += "key: " + song_object["metadata"]["key"] + "\n"
    song_data += "tempo: " + song_object["metadata"]["tempo"] + "\n\n"
    song_data += "font size: " + song_object["fontsize"] + "\n\n"
    for el in song_object["music_lyrics"]:
        song_data += el + "\n\n"
    song_data = song_data[:-2]
    return song_data
