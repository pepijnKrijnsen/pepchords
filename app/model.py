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
    if not "title" in dict or not "artist" in dict:
        return redirect(url_for("addSong"))
    song_uid = _createSongUID(dict["title"], dict["artist"])
    song_data = _unpackSongData(dict)
    persistence.writeSongFile(song_uid, song_data)
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

def _unpackSongForm(dict):
    song_data = dict["title"] + "\n\n"
    song_data += dict["artist"] + "\n\n"
    song_data += "Capo: " + dict["capo"] + "\n"
    song_data += "Key: " + dict["key"] + "\n"
    song_data += "Tempo: " + dict["tempo"] + "\n\n"
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
    song["music_lyrics"] = items
    return song

def editSong(uid):
    song_raw = persistence.readSongFile(uid)
    song = _songRawToDict(song_raw)
    song["uid"] = uid
    song["music_lyrics_string"] = ""
    for el in song["music_lyrics"]:
        song["music_lyrics_string"] += el + "\n\n"
    song["music_lyrics_string"] = song["music_lyrics_string"][:-2]
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
    song_data += dict["music_lyrics"]
    song_data += "Key: " + dict["Key"] + "\n"
    song_data += "Capo: " + dict["Capo"] + "\n\n"
    print(dict["music_lyrics"])
    return song_data
