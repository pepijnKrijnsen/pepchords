def readSongFile_toLines(uid):
    path = "songs/" + uid
    with open(path) as songfile:
        song_lines = songfile.readlines()
    return song_lines

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

def backUpSong(uid):
    system("mv songs/" + uid + " song_backups/" + uid)
    return

def readSecretKeyFile():
    with open("secret_key") as s:
        return s.read()
