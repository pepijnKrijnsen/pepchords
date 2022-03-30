from os import (path, system, listdir)

import persistence

def buildSonglist():
    songlist = []
    for song_file in listdir("songs"):
        songlist.append(_getSongData(song_file))
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

def createSongObject(dict):
    # keys in dict:
    # - title (required)
    # - artist (required)
    # - music_lyrics (optional)
    # - metadata: key, capo, tempo (optional)
    song_uid = _createSongUID(dict["title"], dict["artist"])
    song_data_string = _unpackSongData(dict)
    persistence.writeSongFile(song_uid, song_data_string)
    return

def _createSongUID(title, artist):
    safe_artist = artist.lower().replace(" ", "-")
    safe_artist = _filterScaryChars(safe_artist)
    safe_title = title.lower().replace(" ", "-")
    safe_title = _filterScaryChars(safe_title)
    return safe_artist + "-" + safe_title

def _filterScaryChars(string):
    string = string.replace("'", "")
    string = string.replace("á", "a")
    string = string.replace("é", "e")
    string = string.replace("ï", "i")
    string = string.replace("&-", "")
    return string

def _unpackSongData(dict):
    song_data = dict["title"] + "\n\n"
    song_data += dict["artist"] + "\n\n"
    song_data += "capo: " + dict["capo"] + "\n"
    song_data += "key: " + dict["key"] + "\n"
    song_data += "tempo: " + dict["tempo"] + "\n\n"
    song_data += "font size: 16" + "\n\n"
    song_data += dict["music_lyrics"]
    return song_data

def displaySong(uid):
    song_raw = persistence.readSongFile(uid)
    song = _songRawToDict(song_raw)
    song["uid"] = uid
    return song

def _songRawToDict(song_raw):
    items = song_raw.split("\n\n")
    song = dict()
    song["title"] = items.pop(0)
    song["artist"] = items.pop(0)
    song["metadata"] = dict()
    for line in items.pop(0).split("\n"):
        pair = line.split(": ")
        song["metadata"][pair[0]] = pair[1]
    song["fontsize"] = items.pop(0).split(": ")[1]
    song["music_lyrics"] = items
    return song

def updateFontSize(uid, change):
    song = _songRawToDict(persistence.readSongFile(uid))
    song["fontsize"] = str(float(song["fontsize"]) + (change / 2))
    song_string = _songDictToRaw(song)
    persistence.writeSongFile(uid, song_string)
    return

def _songDictToRaw(song_object):
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

def editSong(uid):
    song_raw = persistence.readSongFile(uid)
    song = _songRawToDict(song_raw)
    song["uid"] = uid
    song["music_lyrics_string"] = ""
    for el in song["music_lyrics"]:
        song["music_lyrics_string"] += el + "\n\n"
    song["music_lyrics_string"] = song["music_lyrics_string"][:-2]
    return song
