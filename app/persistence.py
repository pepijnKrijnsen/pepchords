def readSongFile(path):
    with open(path) as songfile:
        song_raw = songfile.read()
    return song_raw

def writeSongFile(path, content):
    with open(path, "w") as songfile:
        songfile.write(content)
    return
