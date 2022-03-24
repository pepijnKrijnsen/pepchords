from flask import (
        Flask, render_template, redirect, url_for, request
        )

from model import (
        buildSonglist, findSong, createNewSong, parseSong, backUpSong, createSongData,
        )

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", songlist = buildSonglist())

@app.route("/play/<uid>")
def getSong(uid):
    song_object = findSong(uid)
    if song_object:
        # read the song file and create a dictionary
        song = parseSong(song_object)
        song["uid"] = uid
        return render_template("song.html", song = song)
    else:
        # create a new song file
        createNewSong(uid)
        return redirect(url_for("index"))

@app.route("/edit/<uid>")
def edit(uid):
    song = parseSong(findSong(uid))
    song["uid"] = uid
    return render_template("song_attributes.html",
            song = song)

@app.route("/save/<uid>", methods = ["POST", ])
def saveEditsToSong(uid):
    # move the song file from "songs/<uid>" to "songs/backup/<uid>"
    backUpSong(uid)
    # write a new file "songs/<uid>" with the contents of:
    #  - title
    #  - artist
    #  - Key
    #  - Capo
    #  - music_lyrics
    new_file_contents = createSongData(request.form)
    with open("songs/" + uid, "w") as song_file:
        song_file.write(new_file_contents)
    return redirect(url_for("index"))

@app.route("/song/new")
def addNewSong():
    return render_template("song_attributes.html")

@app.route("/song/save", methods = ["POST", ])
def saveNewSong():
    line = request.form["title"] + "," + request.form["artist"] + ",,,,,," + request.form["key"] + "," + request.form["capo"] + ",,0,false" + "\n"
    with open("newsongs.csv", "a") as f:
        f.write(line)
    return redirect(url_for("index"))

@app.route("/practice")
def logPractice():
    return render_template("practice.html", 
            practice_types = getPracticeTypes())

@app.route("/practice/save", methods = ["POST", ])
def savePracticeLog():
    # persistence!
    return redirect(url_for("index"))


def newSongToCsv():
    pass

def getPracticeTypes():
    types = [ "", "stream", "repetition", "new song" ]
    return types
