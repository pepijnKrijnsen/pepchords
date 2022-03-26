def readSongFile(uid):
    path = "songs/" + uid
    with open(path) as songfile:
        song_raw = songfile.read()
    return song_raw

def writeSongFile(uid, content):
    path = "songs/" + uid
    with open(path, "w") as songfile:
        songfile.write(content)
    return
